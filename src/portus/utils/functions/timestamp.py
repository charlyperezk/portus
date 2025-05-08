from datetime import datetime
from typing import List

def add_timestamps(fields: List[str] = ['created_at']) -> dict[str, str]:
        now = datetime.now()
        fields_to_add = {field: now for field in fields}
        return fields_to_add