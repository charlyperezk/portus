from datetime import datetime
from typing import Union

def set_timestamp() -> dict[str, Union[str, datetime]]:
    print("[TransformerFunctions:SetTimeStamp] Setting timestamp.")
    now = datetime.now()
    return {
        'created_at': now,
        'updated_at': now
    }

def set_update_time() -> dict[str, datetime]:
    return {
        'updated_at': datetime.now()
    }