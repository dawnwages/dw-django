release: DJANGO_SETTINGS_MODULE=dawnwagesinfo.settings.deploy python manage.py migrate --noinput && (DJANGO_SETTINGS_MODULE=dawnwagesinfo.settings.deploy python manage.py publish_posts || echo "publish_posts failed; the deploy continues")
web: DJANGO_SETTINGS_MODULE=dawnwagesinfo.settings.deploy gunicorn dawnwagesinfo.wsgi
