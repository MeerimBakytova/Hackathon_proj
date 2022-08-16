import time
from django.core.mail import send_mail

from main.celery import app


def send_confirmation_email(code, email):
    full_link = f'Здравствуйте!' \
                f'Подтвердите свою регистрацию, пройдя по ссылке:' \
                f' http://localhost:8000/api/v1/account/activate/{code}'

    send_mail(
        'From MiniInsta',
        full_link,
        'bshmeerim@gmail.com',
        [email]
    )

@app.task
def send_activation_sms(email, code):
    time.sleep(10)
    send_mail(
        'From MiniInsta',
        f'Ваш активационный код {code}',
        'bshmeerim@gmail.com',
        [email]
    )

