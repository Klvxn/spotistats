FROM python:3.10.4-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /src

COPY requirements.txt /src

RUN pip install --upgrade pip && pip install -r requirements.txt --no-cache-dir

COPY . /src

RUN python3 manage.py migrate
RUN python3 manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "config.wsgi:application", "-b 0.0.0.0:8000"]
