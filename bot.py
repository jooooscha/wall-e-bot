import simplematrixbotlib as botlib
import os
#  import threading
import asyncio
from time import sleep
from datetime import datetime, timedelta, time

import spielerplus

creds = botlib.Creds("https://matrix.serwm.com", "wall-e", "c))2l(CBrt],~=9Yu?XdALjl7[fw+q(Y/`U.SQ3{SrSgY}?bSQ`2%%`[~2K3S0577s@}eIhF6SA$J%+qADG_T?_]RUS,13K")
config = botlib.Config()
config.join_on_invite = True
bot = botlib.Bot(creds, config)
PREFIX = '!'

def seconds_to_next_notification():
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
    if "Joshua" in event_info["pending"]:
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

async def send_event_info(room_id):
    # fetch data
    next_event_info = spielerplus.fetch_next_event()
    formatted_text = format_msg(next_event_info)

    # send message
    await bot.api.send_text_message(room_id, formatted_text)


#  @bot.listener.on_startup
#  async def reminder(room_id):
#      print(f"Wall-e is in room: {room_id}")

#      if room_id != "!SbqqbJBFSbDmSzMjIk:serwm.com":
#          return

    #  while True:
    #      # sleep until next notification
    #      t_wait, t_target = seconds_to_next_notification()
    #      print(f"Waiting {t_wait.total_seconds()}, until {t_target.strftime('%d.%m %H:%M')}")
    #      sleep(t_wait.total_seconds())

    #      await send_event_info(room_id)

@bot.listener.on_message_event
async def info(room, message):
    print("Fetching ingo")
    #  if room.room_id != "!SbqqbJBFSbDmSzMjIk:serwm.com":
    #      print(f"msg in room {room.room_id}")
    #      return

    match = botlib.MessageMatch(room, message, bot, PREFIX)

    if match.is_not_from_this_bot() and match.prefix() and match.command("info"):
        await bot.api.send_text_message(room.room_id, "Fetching info. Please wait...")
        await send_event_info(room.room_id)

def start_bot():
    bot.run()

#  def send_msg(msg, exit_after=False):

#      @bot.listener.on_startup
#      async def room_joined(room_id):
#          print(f"Wall-e is in room: {room_id}")

#          if room_id != "!SbqqbJBFSbDmSzMjIk:serwm.com":
#              return

#          await bot.api.send_text_message(room_id, msg)

#          if exit_after:
#              exit()

