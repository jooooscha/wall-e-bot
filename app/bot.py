import simplematrixbotlib as botlib
from app.bot_helper import *
import os
import sys

STORE_DIR = "/run/wall_e"

content = None
with open(sys.argv[1], "r") as file:
    content = file.read()

if content is None:
    exit(f"Could not read access token file from {sys.argv[1]}")

#  session_path = "/run/wall-e"
if not os.path.exists(STORE_DIR):
    os.makedirs(STORE_DIR)

creds = botlib.Creds(
    homeserver="https://matrix.serwm.com",
    username="wall-e",
    password=content,
    session_stored_file=os.path.join(STORE_DIR, "session.txt")
)
config = botlib.Config()
config.join_on_invite = True
config.encryption_enabled = True
config.emoji_verify = True
config.ignore_unverified_devices = True
config.store_path = STORE_DIR

bot = botlib.Bot(creds, config)
PREFIX = '!'

@bot.listener.on_startup
async def reminder(room_id):
    if room_id == ROOM_ID:
        print(f"Starting reminder for room: {room_id}", flush=True)
        await reminder_thread(bot)

#  @bot.listener.on_message_event
#  async def info(room, message):

#      match = botlib.MessageMatch(room, message, bot, PREFIX)

#      if match.is_not_from_this_bot() and match.prefix() and match.command("info"):
#          print(f"Fetching info ({room.room_id})")
#          await bot.api.send_text_message(room.room_id, "Fetching info. Please wait...")
#          await send_event_info(bot, room.room_id)

#  @bot.listener.on_message_event
#  async def echo(room, message):

#      match = botlib.MessageMatch(room, message, bot, PREFIX)

#      if match.is_not_from_this_bot() and match.prefix() and match.command("ping"):
#          await bot.api.send_text_message(room.room_id, "pong")

def start_bot():
    bot.run()
