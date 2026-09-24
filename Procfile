release: DJANGO_SETTINGS_MODULE=dawnwagesinfo.settings.deploy python manage.py migrate --noinput
web: DJANGO_SETTINGS_MODULE=dawnwagesinfo.settings.deploy gunicorn dawnwagesinfo.wsgi
