# def send_email(_from: str, _to: str, _subject: str, _message: str) -> None:
#     raise NotImplementedError()

def send_welcome_email(data) -> None:
    print(f"[TriggeredAction:MailService:MailSent] Welcome email sent successfully. (Email {data.email})")

def send_update_email(data) -> None:
    print(f"[TriggeredAction:MailService:MailSent] Your user data was updated successfully. (Email {data.email})")