FROM python:3.11.2-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/myapp

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . .

RUN python manage.py migrate

EXPOSE 8080

CMD ["uvicorn", "config.asgi:application", "--port=8080", "--workers=8"]