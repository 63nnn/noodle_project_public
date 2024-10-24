from discord.ext import commands
import json


with open("privateSetting.json") as jfile:
    jj = json.load(jfile)


class Tester(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.__channel = None

    def setup_channel(self):
        self.__channel = self.bot.get_channel(jj["log_channel"])

    @commands.command()
    async def ping(self, ctx):
        await ctx.send("pong")

    @commands.command()
    async def reboot(self, ctx):
        if ctx.message.content.split()[1] == "api":
            import requests
        try:
            _ = requests.get(jj["reboot"])  # call server reboot
        except requests.exceptions.ConnectionError:
            # reboot success
            await self.__channel.send("Rebooting. API server disconnected.")
            if ctx.channel != self.__channel:
                await ctx.send("Rebooting. API server disconnected.")

        else:
            await self.__channel.send("Something went wrong.")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, err):
        await ctx.send(err)


async def setup(bot):
    tester = Tester(bot)
    tester.setup_channel()
    await bot.add_cog(tester)
