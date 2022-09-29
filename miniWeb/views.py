from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
import environ
from .models import dataAtten
import json
from .task import test_fuk
env = environ.Env()
environ.Env.read_env()

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
    print(data)
    return data

# Create your views here.
def getAttendance():
    r = requests.Session()
    print(env('ROLLNO'))
    rollNo = env('ROLLNO')
    password =  env('PASSWORD')

    req1 = r.post(
        f'https://webkiosk.juit.ac.in:9443/CommonFiles/UserAction.jsp?txtInst=Institute&InstCode=JUIT&txtuType=Member+Type&UserType=S&txtCode=Enrollment+No&MemberCode={rollNo}&txtPin=Password%2FPin&Password={password}&BTNSubmit=Submit')

    req2 = r.get('https://webkiosk.juit.ac.in:9443/StudentFiles/Academic/StudentAttendanceList.jsp')

    data = getData(req2)

    completeData = {
        'data': data,
    }
    return completeData



def settings(request):
    return render(request, 'miniWeb/settings.html')

def register(request):
    return render(request, 'miniWeb/register.html')

def login(request):
    return render(request, 'miniWeb/login.html')



def dashboard(request):
    # try:
    #     dataServer = dataAtten.objects.get(username = env('ROLLNO'))
    # except dataAtten.DoesNotExist:
    #     dataServer = None

    data = ''
    # test_fuk.delay()
    # if(dataServer):
    #     data = dataServer.data
    #     data = data.replace("\'", "\"")
    #     data = json.loads(data)
    # else:
    #     data = getAttendance()
    #     dataAtten.objects.create(
    #         username=env('ROLLNO'),
    #         data = data
    #     )

    # test_fuk.delay()
    dataServer = dataAtten.objects.get(username=env('ROLLNO'))
    data = dataServer.data
    data = data.replace("\'", "\"")
    data = json.loads(data)
    return render(request, 'miniWeb/dashboard.html', {'att': data['data']})