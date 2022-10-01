from celery import shared_task
from .models import Profile
from bs4 import BeautifulSoup
import environ
import requests
import json
from django.contrib.auth.models import User

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


def getAttendance(rollNo, password):
    r = requests.Session()
    # print(env('ROLLNO'))
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


@shared_task(bind=True)
def initial_task(self, rollNo, password):

    # dataObj = Profile.objects.get(user = user)

    dataObj = User.objects.get(username=rollNo)
    dataFetch = getAttendance(rollNo, password)
    dataObj.profile.data = dataFetch
    dataObj.profile.save()

    return "DOne"