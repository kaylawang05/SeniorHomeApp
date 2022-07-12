import datetime

def get_time() -> str:
    return datetime.datetime.now().strftime("%H:%M")

def get_date() -> datetime.date:
    return datetime.date.today()
