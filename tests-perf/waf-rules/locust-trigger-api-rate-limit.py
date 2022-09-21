"""locust-trigger-rate-limit.py

Trigger rate limit on our WAF rules for api

Once the necessary rate limit has been attained within a 5 minutes period, the
tests will start to fail as expected.
"""
# flake8: noqa

import os
from dotenv import load_dotenv
from locust import HttpUser, constant_pacing, task

load_dotenv()


class NotifyApiUser(HttpUser):

    host = "https://api.staging.notification.cdssandbox.xyz"
    spawn_rate = 10
    wait_time = constant_pacing(1)  # 20 users will give 1200 requests / minute

    def __init__(self, *args, **kwargs):
        super(NotifyApiUser, self).__init__(*args, **kwargs)
        self.headers = {"waf-secret": os.getenv("WAF_SECRET", "bad-secret-3")}

    @task(1)
    def trigger_api_block(self):
        self.client.get("/_status", headers=self.headers)
