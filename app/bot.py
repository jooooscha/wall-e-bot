import simplematrixbotlib as botlib
from app.bot_helper import *
from time import sleep
import os
from dotenv import load_dotenv
import sys

load_dotenv(sys.argv[1])

creds = botlib.Creds(
    homeserver="https://matrix.serwm.com",
    username="wall-e",
    access_token=os.getenv('ACCESS_TOKEN'),
)
config = botlib.Config()
config.join_on_invite = True
config.encryption_enabled = True
config.emoji_verify = True
config.ignore_unverified_devices = True

bot = botlib.Bot(creds, config)
PREFIX = '!'

@bot.listener.on_startup
async def reminder(room_id):
    print(f"Wall-e is in room: {room_id}")

    # only run in this one room:
    if room_id == "!SbqqbJBFSbDmSzMjIk:serwm.com":
        while True:
            # sleep until next notification
            t_wait, t_target = seconds_to_next_notification()
            print(f"Waiting {t_wait.total_seconds()}, until {t_target.strftime('%d.%m %H:%M')}")
            sleep(t_wait.total_seconds())

            await send_event_info(room_id)

@bot.listener.on_message_event
async def info(room, message):

    match = botlib.MessageMatch(room, message, bot, PREFIX)

    if match.is_not_from_this_bot() and match.prefix() and match.command("info"):
        print(f"Fetching info ({room.room_id})")
        await bot.api.send_text_message(room.room_id, "Fetching info. Please wait...")
        await send_event_info(room.room_id)

@bot.listener.on_message_event
async def echo(room, message):

    match = botlib.MessageMatch(room, message, bot, PREFIX)

    if match.is_not_from_this_bot() and match.prefix() and match.command("ping"):
        await bot.api.send_text_message(room.room_id, "pong")

def start_bot():
    bot.run()
