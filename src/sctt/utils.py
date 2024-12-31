from datetime import datetime, timezone


def convert_utc_to_local(utc_time: str) -> str:
    """Convert UTC time string to local time string.

    Args:
        utc_time (str): UTC time in the format "%Y-%m-%d %H:%M:%S".

    Returns:
        str: Local time in the format "%Y-%m-%d %H:%M:%S".
    """

    utc_dt: datetime = datetime.strptime(utc_time, "%Y-%m-%d %H:%M:%S")
    utc_dt = utc_dt.replace(tzinfo=timezone.utc)
    local_dt: datetime = utc_dt.astimezone()

    return local_dt.strftime("%Y-%m-%d %H:%M:%S")
