from portus.ports.output.notifications import NotificationPort
from portus.common.types import TInternalData
from portus.hooks.triggerer import DataTriggererHook

def email_notification_trigger_hook(
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