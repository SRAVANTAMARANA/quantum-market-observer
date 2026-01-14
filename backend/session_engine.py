import pytz

NY = pytz.timezone("America/New_York")

def ny_session_active(ts):
    ts = ts.tz_localize("UTC").astimezone(NY)
    return 13 <= ts.hour <= 16
