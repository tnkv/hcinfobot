import discord
from discord.commands import Option

import commands
import config

bot = discord.Bot()


@bot.slash_command(name="sinfo", description='Отправить информацию о сервере.', guild_ids=config.guild_ids)
async def first_slash(ctx):
    await ctx.respond((await commands.sinfo()).replace("_", "\_"))


@bot.slash_command(name="info", description='Отправить информацию об игроке.', guild_ids=config.guild_ids)
async def first_slash(ctx, nickname: Option(str, "Введите никнейм", required=True, default='')):
    await ctx.respond(await commands.pinfo(nickname))


bot.run(config.dstoken)
