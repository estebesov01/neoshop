FROM python:3.8.10
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED=1
ENV DEBUG=0
WORKDIR /usr/src/neoshop
COPY requirements.txt /usr/src/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r /usr/src/requirements.txt
COPY . /usr/src/neoshop
RUN python manage.py migrate --noinput
RUN python manage.py collectstatic --noinput


RUN adduser -u 123 nurs
USER nurs

# run gunicorn
CMD gunicorn neoshop.wsgi:application --bind 0.0.0.0:$PORT