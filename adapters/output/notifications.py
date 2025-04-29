from ports.output.notifications import NotificationPort

class Notifications(NotificationPort):
    async def send_email(self, to, subject, body):
        pass
    
    async def send_sms(self, phone_number, message):
        pass