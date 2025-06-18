# optima_back
 
python -m venv

pip install -r requirements.txt

python manage.py migrate --fake optimasite zero

python manage.py makemigrations

python manage.py migrate

python manage.py runserver

python manage.py createsuperuser

py -m pip freeze > requirements.txt

python manage.py collectstatic --clear