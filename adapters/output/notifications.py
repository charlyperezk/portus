from ports.output.notifications import NotificationPort

class Notifications(NotificationPort):
    def send_email(self, to, subject, body):
        print(f"Mail sent to: {to}\nSubject: {subject}\nBody: {body}")
    
    def send_sms(self, phone_number, message):
        pass