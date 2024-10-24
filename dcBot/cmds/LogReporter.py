from discord.ext import commands, tasks
import json
from datetime import date

with open("privateSetting.json") as jfile:
    jj = json.load(jfile)


class LogReporter(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.__channel = None
        self.__today = date.today().strftime("%y%m%d")
        self.__filePath = jj["log_path"]
        self.__open_log_file()
        self.__cursor = 0
        self.logBot.start()

    def setup_channel(self):
        self.__channel = self.bot.get_channel(jj["log_channel"])

    def __open_log_file(self):
        """Open the current log file."""
        # touch, ensure file exist
        with open(
            f"{self.__filePath}API_server.log.csv", "a", encoding="utf-8"
        ) as file:
            pass
        self.__file = open(
            f"{self.__filePath}API_server.log.csv", "r", encoding="utf-8"
        )

    async def date_change(self):
        """Archive old log file then create a new one"""
        import os, requests

        os.rename(
            f"{self.__filePath}API_server.log.csv",
            f"{self.__filePath}{self.__today}API_server.log.csv",
        )
        try:
            _ = requests.get(jj["reboot"])  # call server reboot
        except requests.exceptions.ConnectionError:
            # reboot success
            await self.__channel.send("Daily reboot. API server disconnected.")
        else:
            await self.__channel.send("Something went wrong.")

        self.__file.close()  # Close the old handle file
        self.__today = date.today().strftime("%y%m%d")  # renew date
        self.__open_log_file()  # Open the new log file for reading

    def cog_unload(self):  # when activate unload
        self.logBot.cancel()  # let the loop really cancel
        self.__file.close()  # Close the file when cog unloads

    @tasks.loop(seconds=2)
    async def logBot(self):
        if self.__today != date.today().strftime("%y%m%d"):  # if date change
            await self.date_change()

        try:
            self.__cursor = self.__file.tell()
            line = self.__file.readline()
            # Check if message content is valid
            if line and line.strip():
                await self.__channel.send(line)
            else:  # if line empty
                self.__file.seek(self.__cursor)
        except Exception as e:
            await self.__channel.send("Message is too long.")
            pass

    @logBot.before_loop
    async def before_logBot(self):
        await self.__channel.send(f"Today is {self.__today}")

    @commands.command()
    async def stop(self, ctx=None):
        """stop the loop. (make the function can stop specific loop later)"""
        msg = ""
        if self.logBot.is_running():
            self.logBot.stop()
            msg = "stop logBot"
        else:
            msg = "It's not running."
        if ctx != None:
            await ctx.send(f"{msg}")

    @commands.command()
    async def start(self, ctx=None):
        """start the loop. (make the function can start specific loop later)"""
        msg = ""
        if not self.logBot.is_running():
            self.logBot.start()
            msg = "start logBot"
        else:
            msg = "It's already start."
        if ctx != None:
            await ctx.send(f"{msg}")

    @commands.command()
    async def skip(self, ctx=None):
        if ctx.message.content.split()[1] == "log":
            self.stop(None)
            while True:
                try:
                    self.__cursor = self.__file.tell()
                    line = self.__file.readline()
                    # Check if message content is valid
                    if line and line.strip():
                        pass
                    else:  # if line empty
                        self.__file.seek(self.__cursor)
                        await ctx.send("skip successfully.")
                        break
                except Exception as e:
                    pass
            self.start(None)

    @commands.command()
    async def see(self, ctx):
        print(f"{self.__filePath}{self.__today}API_server.log.csv")

    @commands.command()
    async def __test(self, ctx):
        await self.__channel.send("You are calling the test command.")
        await self.date_change()


async def setup(bot):
    repoter = LogReporter(bot)
    repoter.setup_channel()
    await bot.add_cog(repoter)
