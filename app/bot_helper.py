from datetime import datetime, timedelta, time
from app import spielerplus

async def send_event_info(room_id):
    # fetch data
    next_event_info = spielerplus.fetch_next_event()
    formatted_text = format_msg(next_event_info)

    # send message
    await bot.api.send_text_message(room_id, formatted_text)

def seconds_to_next_notification():
    """ Returns the seconds until the next notification """

    today  = datetime.combine(datetime.now(), time(12, 0))

    next_tue = (1 - today.weekday()) % 7
    next_thu = (3 - today.weekday()) % 7

    if next_tue == 0:
        next_tue = 7

    if next_thu == 0:
        next_thu = 7

    next_date = min(next_tue, next_thu)

    target_time = today + timedelta(days=next_date)

    time_to_wait = target_time - datetime.now()

    return time_to_wait, target_time

def format_msg(event_info):

    res = ""
    if "Joscha" in event_info["pending"]:
        res += "Joscha, du hast dich noch nicht gemeldet\n"
    if "Yoshi" in event_info["pending"]:
        res += "Yoshi, du hast dich noch nicht gemeldet\n"

    if res == "":
        res = "Ihr hab euch beide schon gemeldet. Prima!"

    text = f"""
🏐🏐 Volleyball 🏐🏐

Date: {event_info["date"]}
Type: {event_info["title"]}
Bisher haben {event_info["n_zusage"]} zugesagt und {event_info["n_absage"]} abgesagt. ({event_info["n_unsicher"]} unsicher)

{res}
"""

    return text.strip()
