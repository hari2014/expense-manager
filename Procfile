web: gunicorn app:app --log-file=-
init: python manage.py
heroku ps:scale web=1
