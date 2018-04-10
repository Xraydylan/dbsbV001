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
test_channel = None

async def ex(args, message, client, invoke, server, dbx):
    global status, test_channel
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


                    main_loop = asyncio.get_event_loop()
                    #Start the thread
                    threading.Thread(name='loop_p', target=loop_p, args=(client, message.channel, main_loop)).start()

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

def loop_p(client, channel, main_loop):
    global status
    print ("on")
    counter = 0
    while status == 1:
        main_loop.create_task(sender(client, channel, counter))
        counter += 1
        print("Done")
        time.sleep(30)



async def sender(client, channel, context):
    await client.send_message(channel, context)

