import simplematrixbotlib as botlib
from app.bot_helper import *
from time import sleep

creds = botlib.Creds("https://matrix.serwm.com", "wall-e", "c))2l(CBrt],~=9Yu?XdALjl7[fw+q(Y/`U.SQ3{SrSgY}?bSQ`2%%`[~2K3S0577s@}eIhF6SA$J%+qADG_T?_]RUS,13K")
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

    if room_id != "!SbqqbJBFSbDmSzMjIk:serwm.com":
        return

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
