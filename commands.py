from datetime import datetime, timedelta
from typing import Optional
import aiohttp
import config
import locale

api_link = config.apilink


async def get_session():
    return aiohttp.ClientSession()


async def playerinfo(name: str) -> dict:  # Получения json с информацией об игроке
    session = aiohttp.ClientSession()
    async with session.get(api_link + "player?name=" + name) as resp:
        answer = await resp.json(content_type=None)
        await session.close()
        return answer


async def serverinfo() -> dict:  # получение json с информацией о сервере
    session = aiohttp.ClientSession()
    async with session.get(api_link + "server") as resp:
        answer = await resp.json(content_type=None)
        await session.close()
        return answer


def formattime(value) -> str:  # перевод кол-ва секунд в легко-понимаемое время
    return str(timedelta(seconds=value))


async def getweather(answer) -> str:  # перевожу погоду в читаемый вид + добавляю нужный эмодзи в зависимости от погоды
    if answer["weather"] == "sun":
        return "☀️ Погода: Солнечно"
    elif answer["weather"] == "rain":
        return "🌧 Погода: Дождь"
    elif answer["weather"] == "storm":
        return "⛈ Погода: Гроза"
    else:
        return f"Произошла ошибка при обработке информации о погоде.\nОтвет от сервера: {answer['weather']}"


async def pinfo(name: Optional[str] = None) -> str:
    if name is None:
        return (
            "👹 Некорректное использование. \n\n😊 Необходимо написать ник.\nПример: /info tnkv")  # говорю о
        # необходимости написать ник для получения информации

    answer = await playerinfo(name)  # вызываю функцию получения json'а с инфой об игроке

    wt = answer["player"]["online"]["whitelistTime"]
    if wt == 0:
        wt = "👹 Данный игрок не в вайтлисте"  #
    try:
        locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
    except:
        pass
    else:
        wt = datetime.utcfromtimestamp(wt + 10800).strftime('%d %b. %Y г., %H:%M')
    ts = datetime.utcfromtimestamp(answer["player"]["online"]["last"] + 10800).strftime('%d %b. %Y г., %H:%M')
    # конверчу Unix-Time в читаемый + добавляю 3 часа чтобы бот отвечал в таймзоне МСК
    playtime = formattime(answer["player"]["playtime"])

    msg = f'Информация об игроке:\n\n👨‍💻 Ник: {answer["player"]["name"]}\n⏳ Даты:\nДобавлен: {wt}\nПоследний раз в ' \
          f'сети: {ts}\nПроведено в игре: {playtime}'  # создаю мессаг
    if answer["player"]["team"]["name"] == "-":
        return msg

    return msg + f'\n\n👨‍🏫 Команда: {answer["player"]["team"]["name"]} [{answer["player"]["team"]["tag"]}], Лидер ' \
                 f'команды: {answer["player"]["team"]["leader"]}'
    # добавляю часть к мессагу если игрок участник команды


async def sinfo() -> str:
    answer = await serverinfo()  # вызываю функцию получения json'а с инфой о сервере
    weather = await getweather(answer)  # обработка погоды
    uptime = formattime(answer["uptime_seconds"]).replace('days', 'дней').replace('day', 'день')
    tps = 20 if answer["tps"] >= 20 else answer["tps"]
    # делаю простую проверку на тпс > 20, ибо сервер в случае нестандартного тпс
    # позже нагоняет для того чтобы все работало +- как и должно,
    msg = f'🚀 ТПС: {tps}\n{weather}\n ⏰ Аптайм: {uptime}\n🤵 Онлайн: {answer["online"]}'
    if answer["online"] != 0:
        return msg + f'''\nИгроки онлайн: {answer["players"]}'''
    return msg
