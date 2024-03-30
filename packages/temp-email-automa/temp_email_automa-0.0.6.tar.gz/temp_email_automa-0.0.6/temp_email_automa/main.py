import requests
import random
from typing import Optional
from dataclasses import dataclass


@dataclass
class Email:
    id: str
    sender: str
    subject: str
    date: str
    body: str
    textBody: str
    htmlBody: str


class TempMail:
    """
    Api wraooer provides temporary email address
    :param login: (optimal) login for email address
    :param domain:(optimal) domain for email address
    Default domain 1secmail.com
    """

    def __init__(self, login=None, domain="1secmail.com"):
        self.login = login
        self.domain = domain

    @property
    def email(self):
        if self.login is None or self.domain is None:
            self.generate_random_email_address()
        return f"{self.login}@{self.domain}"

    def generate_random_email_address(self) -> None:
        """Generates random email"""
        r = requests.get(
            "https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=10"
        )
        get_random = f"{random.choice(r.json())}"
        self.login, self.domain = get_random.split("@")

    @property
    def get_list_of_active_domains(self):
        """Return active domains for email address"""
        return requests.get(
            "https://www.1secmail.com/api/v1/?action=getDomainList"
        ).json()

    def get_list_of_emails(self):
        """checks the mailbox for messages and returns them"""
        if self.login is None or self.domain is None:
            self.generate_random_email_address()
        r = requests.get(
            f"https://www.1secmail.com/api/v1/?action=getMessages&login={self.login}&domain={self.domain}"
        )
        return r.json()

    def get_single_email(self, id: int) -> Optional[Email]:
        """Get single email by id"""
        url = f"https://www.1secmail.com/api/v1/?action=readMessage&login={self.login}&domain={self.domain}&id={id}"
        request_response = requests.get(url).json()
        sender = request_response["from"]
        del request_response["from"]
        del request_response["attachements"]
        request_response["sender"] = sender

        return Email(**request_response)
