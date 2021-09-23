from datetime import datetime, timezone

def get_datetime():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()