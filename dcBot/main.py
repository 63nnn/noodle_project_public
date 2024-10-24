import discord as dc
from discord.ext import commands
import os
import json

# Get token
with open("privateSetting.json", "r", encoding="utf8") as jfile:
    jj = json.load(jfile)


intents = dc.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="||", intents=intents)


@bot.event
async def on_ready():
    await load_all_cmds()
    game = dc.CustomActivity("||請問你要一日遊還是二日遊")
    await bot.change_presence(status=dc.Status.online, activity=game)
    print(f"\n>> Now log in: {bot.user}")


# load cmds
@bot.command()
async def load(ctx, *extensions):
    for extension in extensions:
        await bot.load_extension(f"cmds.{extension}")
        await ctx.send(f"Load {extension} done.")


# unload cmds
@bot.command()
async def unload(ctx, *extensions):
    for extension in extensions:
        await bot.unload_extension(f"cmds.{extension}")
        await ctx.send(f"Unload {extension} done.")


# reload cmds
@bot.command()
async def reload(ctx, *extensions):
    for extension in extensions:
        await bot.reload_extension(f"cmds.{extension}")
        await ctx.send(f"Reload {extension} done.")


# bot start function
async def load_all_cmds():
    print("\nstart loading...")
    for cmd in os.listdir("./cmds"):
        if cmd.endswith(".py"):
            try:
                await bot.load_extension(f"cmds.{cmd[:-3]}")
                print(f">> {cmd[:-3]:{15}} loaded successfully")
            except commands.ExtensionAlreadyLoaded:
                print(f">> {cmd[:-3]:{15}} already loaded")


if __name__ == "__main__":
    from aiohttp import ClientConnectionError
    import time

    while True:
        try:
            bot.run(jj["TOKEN"])
        except ClientConnectionError:
            time.sleep(2)
        else:
            break
