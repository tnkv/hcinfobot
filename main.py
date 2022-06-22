from typing import Optional
from vkbottle.bot import Bot, Message
import aiohttp
from datetime import datetime, timedelta

bot = Bot("токен") # токен
api_link = "https://api.hypecloud.ru/vanilla/" # ссылка на апи
 
async def get_session():
    return aiohttp.ClientSession()
 
session = bot.loop.run_until_complete(get_session())
 
async def find_by_nick(name: str) -> dict: # Получения json с информацией об игроке
    async with session.get(api_link+"player?name="+name) as resp:
        answer = await resp.json(content_type=None)
        return answer

async def getsinfo() -> dict: # получение json с информацией о сервере
    async with session.get(api_link+"server") as resp:
        answer = await resp.json(content_type=None)
        return answer

async def formattime(value) -> str: # перевод кол-ва секунд в легко-понимаемое время
    return str(timedelta(seconds = value))

async def getweather(answer) -> str: # перевожу погоду в читаемый вид + добавляю нужный эмодзи в зависимости от погоды
    if answer["weather"] == "sun":
        return "☀️ Погода: Солнечно"
    elif answer["weather"] == "rain":
        return "🌧 Погода: Дождь"
    elif answer["weather"] == "storm":
        return "⛈ Погода: Гроза"
    else:
        return f"Произошла ошибка при обработке информации о погоде.\nОтвет от сервера: {answer[weather]}"


@bot.on.message(text=["/info <name>", "/info"]) # получаю сообщения с командой /info
async def handler(mes: Message, name: Optional[str] = None) -> str:
    if name is None:
        return await mes.answer("👹 Некорректное использование. \n\n😊 Необходимо написать ник.\nПример: /info tnkv") # говорю о необходимости написать ник для получения информации
    answer = await find_by_nick(name) # вызываю функцию получения json'а с инфой об игроке
    wt = answer["player"]["online"]["whitelistTime"]
    if wt == 0:
        return await mes.answer("👹 Некорректное использование. \n\n😊 Данный ник не в вайтлисте") # по ответу определяю в вайтлисте ли игрок и останавливаюсь в случае отсутствия 

    wt = datetime.utcfromtimestamp(wt+10800).strftime('%d.%m.%Y %H:%M:%S') 
    ts = datetime.utcfromtimestamp(answer["player"]["online"]["last"]+10800).strftime('%d.%m.%Y %H:%M:%S') # конверчу Unix-Time в читаемый + добавляю 3 часа чтобы ответ приходил в таймзоне МСК
    playtime = await formattime(answer["player"]["playtime"]) 


    msg = f'Информация об игроке:\n\n👨‍💻 Ник: {answer["player"]["name"]} \n⏳ Даты:\n Добавлен: {wtt}\n Последний раз в сети: {tst}\nПроведено в игре: {playtime}' # создаю мессаг
    if answer["player"]["team"]["name"] == "-":
        return await mes.answer(msg)

    await mes.answer(msg + f'\n\n👨‍🏫 Команда: {answer["player"]["team"]["name"]} [{answer["player"]["team"]["tag"]}], Лидер команды: {answer["player"]["team"]["leader"]}') # добавляю часть к мессагу если игрок участник команды


@bot.on.message(text=["/sinfo"])
async def handler(mes: Message) -> str:
    answer = await getsinfo() # вызываю функцию получения json'а с инфой о сервере
    weather = await getweather(answer) # обработка погоды
    uptime = await formattime(answer["uptime_seconds"])
    if answer["tps"] >= 20:
        tps = 20
    else:
        tps = answer["tps"] # делаю простую проверку на тпс > 20, ибо сервер в случае нестандартного тпс позже нагоняет для того чтобы все работало +- как и должно,
         
    await mes.answer(f'🚀 ТПС: {tps}\n{weather}\n⏰ Аптайм: {uptime}\n🤵 Онлайн: {answer["online"]}\nИгроки онлайн:\n{answer["players"]}') # выдаю месаг


bot.run_forever() # запускаю бота
