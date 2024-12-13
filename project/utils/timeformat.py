from datetime import datetime, tzinfo

def get_readable_time(seconds: int) -> str:
    return datetime.fromtimestamp(seconds).strftime("%d-%m-%Y")
