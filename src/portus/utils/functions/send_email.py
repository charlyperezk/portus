# def send_email(_from: str, _to: str, _subject: str, _message: str) -> None:
#     raise NotImplementedError()

async def send_welcome_email(data, service = "MailService") -> None:
    print(f"[TriggeredAction:{service}:MailSent] Welcome email sent successfully. (Email {data.email})")

async def send_update_email(data, service = "MailService") -> None:
    print(f"[TriggeredAction:{service}:MailSent] Your user data was updated successfully. (Email {data.email})")