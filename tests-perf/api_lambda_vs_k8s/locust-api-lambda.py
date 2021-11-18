""" locust-api-lambda.py
    isort:skip_file
"""
# flake8: noqa

import os
import sys
from datetime import datetime
from dataclasses import make_dataclass

sys.path.append(os.path.abspath(os.path.join("..", "tests_smoke")))

from dotenv import load_dotenv
from locust import HttpUser, constant_pacing, task

load_dotenv()
NotifyApiUserTemplateGroup = make_dataclass(
    "NotifyApiUserTemplateGroup",
    [
        "bulk_email_id",
        "email_id",
        "email_with_attachment_id",
        "email_with_link_id",
        "sms_id",
    ],
)


class NotifyApiUser(HttpUser):

    wait_time = constant_pacing(60)  # each user waits at least a minute between emails

    def __init__(self, *args, **kwargs):
        super(NotifyApiUser, self).__init__(*args, **kwargs)
        self.headers = {"Authorization": os.getenv("TEST_AUTH_HEADER")}
        self.email = os.getenv("PERF_TEST_EMAIL", "simulate-delivered@notification.canada.ca")

    @task(16)
    def send_email_notifications(self):
        json = self.__email_json("9544dc32-9d23-4bdd-a8d8-81b4ec9e0485")
        self.client.post("/v2/notifications/email", json=json, headers=self.headers)

    def __email_json(self, template_id, personalisation={"var": "hi"}):
        return {
            "email_address": self.email,
            "template_id": template_id,
            "personalisation": personalisation,
        }
