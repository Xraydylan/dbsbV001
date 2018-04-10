import discord
from discord import Game, Embed
from os import path

async def error(content, channel, client):
    await client.send_message(channel, embed=Embed(color=discord.Color.red(), description=content))

async def assign_role(rolename, message, client, channel, member, server):
    role = discord.utils.get(server.roles, name=rolename)
    if role == None:
        await error("Something went wrong with the role assignment", message.channel, client)
    else:
        if role in member.roles:
            await error("You already have that role.", message.channel, client)
            return False
        else:
            await client.add_roles(member, role)
            await client.send_message(member, embed=discord.Embed(color=discord.Color.green(), description="Congratulations for your new role. \nYou are now part of: \n%s!" % role.name))
            return True
    return None


def exist_all_folders(dbx, path):
    res = dbx.files_list_folder(path)
    count = 0
    for file in res.entries:
        count += 1
    return count

async def dev_authorisation_type1(server, member):
    if path.isfile("data/permission_type1.txt"):
        with open("data/permission_type1.txt") as f:
            content = f.readlines()
            content = [x.strip() for x in content]
            f.close()
        for x in member.roles:
            if x.name in content:
                return True
    return False