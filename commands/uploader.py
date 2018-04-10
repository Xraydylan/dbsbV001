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
from os import path
from datetime import datetime

status = 0
send_channel = None

send_status = 0
send_time = (12,19)

async def ex(args, message, client, invoke, server):
    global status, send_channel
    dbx = dropbox.Dropbox(CONECT.DROP_TOKEN)
    if use.exist_all_folders(dbx,"/Pictures") == 3:
        if len(args) > 0:
            args_out = args.__str__()[1:-1].replace("'", "").replace(",", "")
            if args_out == "ping up":
                await client.send_message(message.channel, "Up Pong!")
            elif args_out == "reset info":
                await reset_info(dbx,client,message.channel)
            elif args_out == "upload count":
                await get_upload_count(dbx,client,message.channel)
            elif args_out == "send":
                await send(dbx,client,message.channel)


            elif args_out == "status":
                if status == 0:
                    content = "The Autouploader is off."
                else:
                    content = "The Autouploader is on."
                await client.send_message(message.channel, content)


            elif args_out == "start":
                if status == 0:
                    await check_for_channel_file(dbx, client, message.channel)
                    if send_channel != None:
                        content = "Starting uploader."
                        status = 1


                        main_loop = asyncio.get_event_loop()

                        #Start the thread
                        threading.Thread(name='sender_loop', target=sender_loop, args=(client, message.channel, main_loop, dbx)).start()

                    else:
                        content = "There is no channel set."

                else:
                    content = "The Autouploader is already on."
                await client.send_message(message.channel, content)


            elif args_out == "stop":
                if status == 0:
                    content = "The Autouploader is already off."
                else:
                    content = "Stopping uploader."
                    status = 0
                await client.send_message(message.channel, content)

            elif args_out == "set":
                await set_channel(dbx, client, message.channel)


    else:
        await client.send_message(message.channel, "There is a storage problem. Folders are missing!")



def increase_down_count(dbx):
    metadata, f = dbx.files_download('/' + "Pictures/info/name_info.txt")
    numbers = str(f.content).replace("b", "").replace("'", "").split("\\r\\n")
    lastn = int(numbers[len(numbers)-1])+1
    out = open("data/info.txt", 'wb')
    out.write(f.content)
    out.close()
    txt = open("data/info.txt", 'w')
    txt.write(str(lastn))
    txt.close()
    up = open("data/info.txt", 'rb')
    dbx.files_upload(up.read(), "/Pictures/info/name_info.txt", mode=WriteMode('overwrite'))
    up.close()
    os.remove("data/info.txt")
    return lastn

async def reset_info(dbx,client,channel):
    await client.send_message(channel, "Info reseted")
    metadata, f = dbx.files_download('/' + "Pictures/info/name_info_reset.txt")
    out = open("data/info_reset.txt", 'wb')
    out.write(f.content)
    out.close()
    up = open("data/info_reset.txt", 'rb')
    dbx.files_upload(up.read(), "/Pictures/info/name_info.txt", mode=WriteMode('overwrite'))
    up.close()
    os.remove("data/info_reset.txt")

async def send(dbx,client,channel):
    res = dbx.files_list_folder("/Pictures/main")
    file_list = []
    for file in res.entries:
        file_list.append(file.name)

    if len(file_list) > 0:
        send_name = random.choice(file_list)

        metadata, f = dbx.files_download('/Pictures/main/' + send_name)

        savepath = "data/temp/" + send_name
        out = open(savepath, 'wb')
        out.write(f.content)
        out.close()

        await client.send_file(channel, savepath)
        from_path = "/Pictures/main/" + send_name
        to_path = "/Pictures/output/" + send_name

        dbx.files_move_v2(from_path, to_path, allow_shared_folder=False, autorename=True)

        os.remove("data/temp/"+send_name)
        increase_down_count(dbx)
    else:
        print ("Empty")

async def get_upload_count(dbx,client,channel):
    metadata, f = dbx.files_download('/' + "Pictures/info/name_info.txt")
    out = open("data/info.txt", 'wb')
    out.write(f.content)
    out.close()

    with open("data/info.txt") as f:
        content = f.readlines()
        content = [x.strip() for x in content]
        await client.send_message(channel, "%s pictures have been uploaded." % content[0])

    os.remove("data/info.txt")



async def set_channel(dbx, client, channel):
    global send_channel
    path_channel = "data/temp/channel.txt"
    channel_id = channel.id
    path_dbx = "/Pictures/info/channel.txt"

    #if not path.isfile(path_channel):

    f = open(path_channel, "w")
    f.write(str(channel_id))
    f.close()

    up = open(path_channel, 'rb')
    dbx.files_upload(up.read(), path_dbx, mode=WriteMode('overwrite'))
    up.close()

    send_channel = channel


async def check_for_channel_file(dbx, client, channel):
    global send_channel
    path_channel = "data/temp/channel.txt"
    path_dbx = "/Pictures/info/channel.txt"

    try:
        metadata, f = dbx.files_download(path_dbx)
        out = open(path_channel, 'wb')
        out.write(f.content)
        out.close()
    except:
        print("No online file")


    if not path.isfile(path_channel):
        await client.send_message(channel, "No channel was previously set.")
    else:
        with open(path_channel) as f:
            content = f.readlines()
            content = [x.strip() for x in content]
            f.close()

        channel_f = client.get_channel(int(content[0]))
        send_channel = channel_f



def sender_loop(client, channel, main_loop, dbx):
    global send_channel, status, send_time

    while status == 1:

        if check_for_time(send_time):
            main_loop.create_task(send(dbx,client,send_channel))

        time.sleep(60)


def check_for_time(send_time):
    global send_status
    ti = str(datetime.utcnow()).split(" ")[1].split(":")[0:2]
    ti[1] = int(ti[1])
    ti[0] = int(ti[0]) + 2
    if ti[0] > 24:
        ti[0] -= 24


    #Not corrected
    if send_time[0] == ti[0] and send_time[1] <= ti[1] and send_time[1] + 2 >= ti[1]:
        if send_status == 0:
            send_status = 1
            return True

    if send_time[0] == ti[0] and send_time[1] + 5 <= ti[1] and send_time[1] + 7 >= ti[1]:
        send_status = 0
    return False
