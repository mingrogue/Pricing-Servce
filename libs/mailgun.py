import os
from typing import List
from requests import Response, post


class MailgunException(Exception):
    def __init__(self, message: str):
        self.message = message


class Mailgun():


    FROM_TITLE = 'Pricing service'
    FROM_EMAIL = 'do-not-reply@sandboxf322d27f530043f1b1b9ecc3f9ef2c10.mailgun.org'

    @classmethod
    def send_mail(cls, email: List[str], subject: str, text: str) -> Response:
        api_key = os.environ.get('MAILGUN_API_KEY', None)
        domain = os.environ.get('MAILGUN_DOMAIN', None)
        if api_key is None:
            raise MailgunException('Falied to load Mailgun Api key')

        if domain is None:
            raise MailgunException('Falied to load Mailgun Api domain')

        response = post(f"{domain}/messages",
                        auth=("api", api_key),
                        data={"from": f"{cls.FROM_TITLE} <{cls.FROM_EMAIL}>",
                              "to": email,
                              "subject": subject,
                              "text": text})
        if response.status_code != 200:
            raise MailgunException('An error occoured sending email')
        return response
