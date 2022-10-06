# AttendanceTracker

Automatically Fetches Attendance (only for JUIT Students)!

## Run Locally 

- You should have Python 3.8 or higher installed.

### First Steps

```sh
git clone https://github.com/vaaibhavsharma/AttendanceTracker.git
cd AttendanceTracker
python3 -m venv env
.\env\Scripts\activate
pip install -r requirements.txt
```

### Environment Variables

Make file .env inside juitWebkiosk with following content

```sh
DEBUG=True
SECRET_KEY= # Put your Django project secret key here - keep it secret!
```

### Django Configurations

```sh
python manage.py makemigrations
python manage.py migrate
python manage.py runserver 8080
```

### Celery Configurations

#### Step 1
Open Another terminal with same environment (python)

```shell
celery -A juitWebkiosk beat -l INFO
```

#### Step 2
On another Terminal
```shell
celery -A juitWebkiosk worker --pool=solo -l INFO
```

Your local instance will now be up and running at http://127.0.0.1:8080/
