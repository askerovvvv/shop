import time

from celery import shared_task
from django.core.mail import send_mail

# @shared_task
from shop.celery import app


@app.task
def send_confirmation_email(code, email):
    full_link = f"http://localhost:8000/api/v1/account/activate/{code}"
    time.sleep(3)
    send_mail( # встроенная функция DJANGO
        'Привет', # title
        full_link, # body
        'bekbol.2019@gmail.com',  # from email
        [email] # to email
    )






