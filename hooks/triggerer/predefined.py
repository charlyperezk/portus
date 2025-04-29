from ports.output.notifications import NotificationPort
from common.types import TInternalData
from hooks.triggerer import DataTriggererHook

def make_email_notification_trigger_hook(
        notification_service: NotificationPort,
        subject: str,
        body: str,
        email_field_in_data: str = "email"
) -> DataTriggererHook:
    async def trigger(data: TInternalData):
        await notification_service.send_email(
            to=data.get_value(email_field_in_data), 
            subject=subject,
            body=body
        )
        return data
    return DataTriggererHook(trigger)