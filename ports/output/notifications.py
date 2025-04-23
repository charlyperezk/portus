from abc import ABC, abstractmethod

class NotificationPort(ABC):
    """
    Port for sending notifications (email, SMS, etc.).
    """
    @abstractmethod
    def send_email(self, to: str, subject: str, body: str) -> None: ...

    @abstractmethod
    def send_sms(self, phone_number: str, message: str) -> None: ...