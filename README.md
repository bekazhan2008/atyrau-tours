first create venv:
python -m venv venv/py -m venv venv

then ectivate it:
venv\Scripts\activate //Windows
//or
source venv\Scripts\activate.bat //MacOS

then install requirements:
pip install -r requirements.txt

after all make migrations and create super user
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser

finally run server:
python manage.py runserver
