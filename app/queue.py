import random

from abc import ABC, abstractmethod
from app import models
from faker import Faker
from faker.providers import BaseProvider
from typing import Any
from uuid import uuid4


# TODO: Move data generation into another module, similar to app.aws.mocks?
fake = Faker()


class NotifyProvider(BaseProvider):
    """Faker provider for the Notify namespace."""

    NOTIFICATION_STATUS = [
        models.NOTIFICATION_CREATED,
        models.NOTIFICATION_SENDING,
        models.NOTIFICATION_SENT,
        models.NOTIFICATION_DELIVERED,
    ]

    SERVICES = [
        "Chair department",
        "Desk department",
        "Pencil department (deprecated)",
        "Gather.town virtual folks",
        "Snowstorm alerting service",
    ]

    def notification(self) -> models.Notification:
        created_at = fake.date_time_this_month()
        email = "success@simulator.amazonses.com"
        data = {
            "id": uuid4(),
            "to": "success@simulator.amazonses.com",
            "job_id": None,
            "job": None,
            "service_id": uuid4(),
            "service": self.service(),
            "template_id": uuid4(),
            "template_version": 1,
            "status": self.status(),
            "reference": uuid4(),
            "created_at": created_at,
            "sent_at": None,
            "billable_units": None,
            "personalisation": {},
            "notification_type": self.notification_type(),
            "api_key": None,
            "api_key_id": None,
            "key_type": None,
            "sent_by": self.provider(),
            "updated_at": created_at,
            "client_reference": None,
            "job_row_number": None,
            "rate_multiplier": None,
            "international": False,
            "phone_prefix": None,
            "normalised_to": email,
            "reply_to_text": self.email(),
            "created_by_id": None,
            "postage": None,
        }
        return models.Notification(**data)

    def notification_type(self) -> str:
        """Gets a random notification type."""
        return random.choice(models.NOTIFICATION_TYPE)

    def provider(self) -> str:
        """Gets a random provider."""
        return random.choice(models.PROVIDERS)

    def service(self) -> str:
        """Gets a random service name"""
        return random.choice(self.SERVICES)

    def status(self) -> str:
        """Gets a random notification status."""
        return random.choice(self.NOTIFICATION_STATUS)


fake.add_provider(NotifyProvider)


def generate_notification(self):
    while True:
        yield fake.notification()


class Queue(ABC):
    """Queue interface for custom buffer.

    Implementations should allow to poll from the queue and acknowledge
    read messages once work is done on these.
    """

    @abstractmethod
    def poll(self, count=10) -> list[Any]:
        """Gets messages out of the queue.

        Args:
            count (int, optional): Number of messages to get out of the queue. Defaults to 10.
        Returns:
            list[Any]: List of messages in the queue, from 1 up to {count} number.
        """
        pass

    @abstractmethod
    def acknowledge(self, message_ids: list[int]):
        """Acknowledges reception and processing of provided messages IDs.

        Once the acknowledgement is done, the messages will get their in-flight
        status removed and will not get served again through the `poll` method.

        Args:
            message_ids (list[int]): [description]
        """
        pass


# TODO: Check if we want to move the queue API and implementations into the utils project.
class RedisQueue(Queue):
    """Implementation of a queue using Redis."""

    def poll(self, count=10) -> list[Any]:
        pass

    def acknowledge(self, message_ids: list[int]):
        pass


class MockQueue(Queue):
    """Implementation of a queue that spits out randomly generated notifications.

    Do not use in production!"""

    def poll(self, count=10) -> list[Any]:
        return [generate_notification() for i in range(0, count)]

    def acknowledge(self, message_ids: list[int]):
        pass
