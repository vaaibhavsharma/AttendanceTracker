from django.shortcuts import render, redirect
import requests
from bs4 import BeautifulSoup
import environ
from .models import dataAtten
import json

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Profile
from .task import initial_task
env = environ.Env()
environ.Env.read_env()
#
# r = requests.Session
# ()
r = requests.Session()
def invalidCheck(req):
    try:
        soup = BeautifulSoup(req.content, "html.parser")
        table = soup.find('font')
        if table.text.strip() == "Invalid Password":
            return False
        else:
            return True
    except:
        return True

def getData(req):
    soup = BeautifulSoup(req.content, "html.parser")
    table = soup.find('table', attrs={'class': 'sort-table'})
    table_body = table.find('tbody')
    rows = table_body.find_all('tr')
    data = []
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        att = []
        for ele in cols:
            if ele:
                try:
                    att.append(float(ele))
                except:
                    att.append(ele)

        data.append(att)
    # data = sorted(data, key = lambda data: data[2], reverse=True)
    # print(data)
    return data


def getPersonalData(req):
    soup = BeautifulSoup(req.content, "html.parser")
    table = soup.find('table')
    rows = table.find_all('tr')
    data = []
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele])
    return data

# Create your views here.
def getAttendance(rollNo, password):
    r = requests.Session()
    # print(rollNo, password)
    # rollNo = env('ROLLNO')
    # password =  env('PASSWORD')

    req1 = r.post(
        f'https://webkiosk.juit.ac.in:9443/CommonFiles/UserAction.jsp?txtInst=Institute&InstCode=JUIT&txtuType=Member+Type&UserType=S&txtCode=Enrollment+No&MemberCode={rollNo}&txtPin=Password%2FPin&Password={password}&BTNSubmit=Submit')

    req2 = r.get('https://webkiosk.juit.ac.in:9443/StudentFiles/Academic/StudentAttendanceList.jsp')

    data = getData(req2)

    completeData = {
        'data': data,
    }
    return completeData


@login_required()
def settings(request):
    return render(request, 'miniWeb/settings.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            rollNo = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            req1 = r.post(
                f'https://webkiosk.juit.ac.in:9443/CommonFiles/UserAction.jsp?txtInst=Institute&InstCode=JUIT&txtuType=Member+Type&UserType=S&txtCode=Enrollment+No&MemberCode={rollNo}&txtPin=Password%2FPin&Password={password}&BTNSubmit=Submit')
            req2 = r.get('https://webkiosk.juit.ac.in:9443/StudentFiles/PersonalFiles/StudPersonalInfo.jsp')
            print(req2.text)
            if invalidCheck(req1) == False:
                return redirect('register')


            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'],
                                    )
            initial_task.delay(rollNo, password)
            login(request, new_user)
            # data = getPersonalData(req2)
            profile = new_user.profile

            try:
                # profile.name = data[1][1]
                profile.webKioskPassword = password
                profile.email = f'{rollNo}@juitsolan.in'
                profile.save()
            except:
                print("No Profile Updated!")
                pass

            return redirect('dashboard')

    context = {}
    form = UserCreationForm()
    context = {'form': form}
    return render(request, 'miniWeb/register.html', context)

def userlogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')

    context = {}

    return render(request, 'miniWeb/login.html', context)


def refreshAtten(request):
    dataServer = Profile.objects.get(user=request.user)
    data = getAttendance(request.user, dataServer.webKioskPassword)
    dataServer.data = data
    dataServer.save()
    return render(request, 'miniWeb/dashboard.html', {'att': data['data']})

def logoutPage(request):
    logout(request)
    return redirect('login')

@login_required()
def dashboard(request):
    dataServer = Profile.objects.get(user=request.user)

    data = dataServer.data
    if data == None:
        return render(request, 'miniWeb/dashboard.html', {'att': "NO"})
    data = data.replace("\'", "\"")
    data = json.loads(data)
    return render(request, 'miniWeb/dashboard.html', {'att': data['data']})

    # if dataServer.data:
    #     data = dataServer.data
    #     data = data.replace("\'", "\"")
    #     data = json.loads(data)
    #     return render(request, 'miniWeb/dashboard.html', {'att': data['data']})
    # else:
    #     # data = getAttendance(request.user, dataServer.webKioskPassword)
    #     # dataServer.data = data
    #     # dataServer.save()
    #     # data = data['data'].replace("\'", "\"")
    #     # data = json.loads(data)
    #     return render(request, 'miniWeb/dashboard.html', {'att': data['data']})





