import discord
import config
import commands

class DSbot(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        # don't respond to ourselve
        if message.author == self.user:
            return

        if message.content == '/sinfo':
            sinfo = await commands.sinfo()
            sinfo = sinfo.replace("_", "\_")
            await message.channel.send(sinfo)
        if "/info" in message.content and not "/sinfo" in message.content:
            msg = message.content.split(" ")
            if len(msg) == 2:
                print(msg[1])
                pinfo = await commands.pinfo(msg[1])
            else:
                pinfo = await commands.pinfo()
            await message.channel.send(pinfo)
            
intents = discord.Intents.default()
intents.message_content = True
client = DSbot(intents=intents)
client.run(config.dstoken()) # запускаю дс бота