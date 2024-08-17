FROM python:3.12.3

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE app_point_system.settings

WORKDIR /../app_point_system

COPY requirements.txt /../app_point_system/
# RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /../app_point_system/

EXPOSE 8000

RUN python manage.py migrate
# RUN python manage.py collectstatic --noinput

CMD ["gunicorn", "--config", "gunicorn_config.py", "app_point_system.wsgi:application"]
