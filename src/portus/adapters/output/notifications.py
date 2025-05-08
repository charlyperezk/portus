from logging import Logger
from portus.ports.output.notifications import NotificationPort

class Notifications(NotificationPort):
    def __init__(self, logger: Logger):
        self.logger = logger or print

    async def send_email(self, to, subject, body):
        self.logger.info(f"Email sent - To: {to} / Subject: {subject}")
    
    async def send_sms(self, phone_number, message):
        self.logger.info(f"SMS sent - To: {phone_number} / Subject: {message}")