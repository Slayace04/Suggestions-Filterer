""""
Copyright © Krypton 2021 - https://github.com/kkrypt0nn (https://krypt0n.co.uk)
Description:
This is a template to create your own discord bot in python.

Version: 4.1
"""
import os
import platform

import disnake
from disnake.ext.commands import Bot

TOKEN: str = ""  # Your bot token from the Discord Developer Dashboard
CARLBOT: int = 0  # Carl bot user ID
SUGGESTIONS_CHANNEL: int = 0  # ID of channel suggestions are posted in
SUGGESTIONS_QUEUE_CHANNEL: int = 0  # ID of the suggestions queue channel
CONSIDERED_CHANNEL: int = 0  # ID of the considered suggestions channel
bot = Bot(intents=disnake.Intents.default())


@bot.event
async def on_ready() -> None:
    print(f"Logged in as {bot.user.name}")
    print(f"disnake API version: {disnake.__version__}")
    print(f"Python version: {platform.python_version()}")
    print(f"Running on: {platform.system()} {platform.release()} ({os.name})")
    print("-------------------")


@bot.event
async def on_message(message: disnake.Message) -> None:
    suggestQueue = bot.get_channel(SUGGESTIONS_QUEUE_CHANNEL)
    if message.author.id == CARLBOT and message.embeds and message.channel.id == SUGGESTIONS_CHANNEL:
        await suggestQueue.send(embed=message.embeds[0])


@bot.event
async def on_raw_message_edit(payload: disnake.RawMessageUpdateEvent) -> None:
    msg: disnake.Message
    if payload.cached_message:
        msg = payload.cached_message
    else:
        msg = await bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
    considered = bot.get_channel(CONSIDERED_CHANNEL)
    if msg.embeds and msg.channel.id == SUGGESTIONS_CHANNEL:
        title = msg.embeds[0].title.lower()
        print("Edited raw, content now: ", title)
        if title.endswith("approved") or title.endswith("denied") or title.endswith("implemented"):
            suggNo = title[title.index("#") + 1:title.index(" ", title.index("#") + 1)]
            await find_and_delete_suggestion(suggNo, SUGGESTIONS_QUEUE_CHANNEL)
            await find_and_delete_suggestion(suggNo, CONSIDERED_CHANNEL)
        elif title.endswith("considered"):
            await considered.send(embed=msg.embeds[0])
            suggNo = title[title.index("#") + 1:title.index(" ", title.index("#") + 1)]
            await find_and_delete_suggestion(suggNo, SUGGESTIONS_QUEUE_CHANNEL)


async def find_and_delete_suggestion(suggestion_no: int, channel_id: int) -> None:
    async for msg in bot.get_channel(channel_id).history():
        if msg.embeds and msg.embeds[0].title.startswith("Suggestion #" + str(suggestion_no)):
            print("Deleted ", msg.embeds[0].title, " from ", channel_id)
            await msg.delete()
            break


# Run the bot with the token
bot.run(TOKEN)

#Made By Slayace04#1000 & Suffocate#6660
