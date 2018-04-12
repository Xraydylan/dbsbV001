import discord
from discord import Game, Embed
from os import path
import CONECT
import STATICS
from use import use,get
import time
from commands_2 import uploader
import asyncio





n_server = None
bot_status = 0
channel_test = None




client_2 = discord.Client()

commands_2 = {

    "uploader": uploader,
}

@client_2.event
async def on_ready():
    global n_server
    print("Bot is logged in successfully. Running on servers:\n")
    for s in client_2.servers:
        print("  - %s (%s)" % (s.name, s.id))
        if str(s.id) == CONECT.SERVER_ID:
            n_server = s
            print(n_server.name)
            bot_status = 1
    if n_server == None:
        print("No matching server found!")
    await uploader.re_status(client_2, asyncio.get_event_loop(), n_server)



@client_2.event
async def on_message(message):
    global n_server
    if message.content.startswith(STATICS.PREFIX):
        invoke = message.content[len(STATICS.PREFIX):].split(" ")[0]
        args = message.content.split(" ")[1:]
        if commands_2.__contains__(invoke):
            await commands_2.get(invoke).ex(args, message, client_2, invoke, n_server)


client_2.run(CONECT.TOKEN2)




