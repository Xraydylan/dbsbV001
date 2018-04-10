import dropbox
from dropbox.files import WriteMode
import discord
import CONECT
import os
import random
from commands import auto_uplader
from use import use

async def ex(args, message, client, invoke, server):
    print("Drop")
    dbx = dropbox.Dropbox(CONECT.DROP_TOKEN)
    if use.exist_all_folders(dbx,"/Pictures") == 3:
        if len(args) > 0:
            args_out = args.__str__()[1:-1].replace("'", "").replace(",", "")
            if args_out == "ping":
                await client.send_message(message.channel, "Pong!")
            elif args_out == "reset info":
                await reset_info(dbx,client,message.channel)
            elif args_out == "upload count":
                await get_upload_count(dbx,client,message.channel)
            elif args_out == "send":
                await send(dbx,client,message.channel)
            elif args_out.split(" ")[0] == "uploader":
                await auto_uplader.ex(args, message, client, invoke, server, dbx)

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

