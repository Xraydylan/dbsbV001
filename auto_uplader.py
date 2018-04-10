import dropbox
from dropbox.files import WriteMode
import discord
import CONECT
import os
import random
from use import use
import time
import threading
import asyncio

status = 0
event = asyncio.get_event_loop()

async def ex(args, message, client, invoke, server, dbx):
    global status
    print("Drop up")
    if use.exist_all_folders(dbx ,"/Pictures") == 3:
        if len(args) > 0:
            args_out = args.__str__()[1:-1].replace("'", "").replace(",", "")
            if args_out == "uploader status":
                if status == 0:
                    content = "The Autouploader is off."
                else:
                    content = "The Autouploader is on."
                await client.send_message(message.channel, content)

            elif args_out == "uploader start":
                if status == 0:
                    content = "Starting uploader."
                    status = 1

                    #Start the thread
                    threading.Thread(name='init', target=init, args=(client, message.channel)).start()

                else:
                    content = "The Autouploader is already on."
                await client.send_message(message.channel, content)

            elif args_out == "uploader stop":
                if status == 0:
                    content = "The Autouploader is already off."
                else:
                    content = "Stopping uploader."
                    status = 0
                await client.send_message(message.channel, content)
    else:
        await client.send_message(message.channel, "There is a storage problem. Folders are missing!")


def init(client, channel):
    global event
    loop = event
    loop.run_until_complete(loop_p(client,channel))
    loop.close()

async def loop_p(client, channel):
    global status
    print ("on")
    await sender(client,channel)
    while status == 1:
        print ("loppy %s" % str(status))

        time.sleep(5)
        print("Done")
        break


async def sender(client, channel):
    await client.send_message(channel, "Workng....")