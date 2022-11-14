from typing import Optional
from vkbottle.bot import Bot, Message
import config
import commands
import logging

logging.getLogger("vkbottle").setLevel(logging.INFO)
vkbot = config.vkbot() # токен
api_link = config.apilink() # ссылка на апи
 
@vkbot.on.message(text=["/info <name>", "/info"]) # получаю сообщения с командой /info
async def playerinfo(mes: Message, name: Optional[str] = None) -> str:
    await mes.answer(await commands.pinfo(name)) # добавляю часть к мессагу если игрок участник команды


@vkbot.on.message(text=["/sinfo"])
async def serverinfo(mes: Message) -> str:
    await mes.answer(await commands.sinfo())

vkbot.run_forever() # запускаю вк бота
