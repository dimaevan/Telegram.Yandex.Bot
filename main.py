import pprint
from dataclasses import dataclass
from config import data_config
from collections import deque
from parser import scraper
from logger import log
import asyncio
import aiohttp
import db

my_config = data_config()
host = "https://api.telegram.org"
words = {'/start': "Привет, Я бот, отправляющий последнюю новость с vc.ru"}
updates = deque()


@dataclass
class Update:
    from_id: int
    date: int
    text: str
    chat_id: int
    update_id: int
    message_id: int

    def __repr__(self):
        return str(f"{self.text} {self.update_id}")


def build_query(method, host_url=host, token=my_config["bot"]["token"]):
    return f"{host_url}/bot{token}/{method}"


def pars(data: list) -> None:
    for element in data:
        if element.get("my_chat_member"):
            key = 'my_chat_member'
        else:
            key = "message"
        x = Update(from_id=element[key]["from"]["id"],
                   chat_id=element[key]['chat']['id'],
                   date=element[key]['date'],
                   text=element[key].get('text'),
                   message_id=element[key].get("message_id"),
                   update_id=element['update_id'],

                   )
        updates.append(x)


async def init():
    async with aiohttp.ClientSession() as session:
        url = build_query("getMe")
        async with session.get(url) as resp:
            response = await resp.json()
            if response['ok'] is True:
                log.info('Bot is ok!')


async def answer(text, chat_id, session):
    url = build_query("sendMessage")
    params = {"chat_id": chat_id}
    last_news_link = db.get_last()

    if text == "/start":
        db.insert_chat(chat_id)
        params.update({"text": words.get(text)})
        await session.get(url, params=params)
        params.update({"text": f"Лови {last_news_link}"})
        await session.get(url, params=params)
    else:
        params.update({"text": f"{last_news_link}"})
        await session.get(url, params=params)

    log.info(f"Answer to chat:{chat_id} {params.get('text')}")


async def poller(session):
    offset = 0
    log.info("Poller starting")
    url = build_query("getUpdates")
    while True:
        params = {"offset": offset}
        async with session.get(url, params=params) as resp:
            response = await resp.json()
        if response.get("ok"):
            pars(response.get("result"))
        if updates:
            offset: Update = updates[-1].update_id + 1
            x: Update = updates.popleft()
            asyncio.create_task(answer(x.text, x.chat_id, session))


async def check_update(session):
    last_link = db.get_last()
    while True:
        new_link_url = db.get_last()
        log.info("Check update")
        if last_link != new_link_url:
            chats = db.get_chats()
            for chat in chats:
                await answer("/last", chat, session)
            db.update_link()
        else:
            log.info("No update")
        await asyncio.sleep(100)


async def main(update=1):
    async with aiohttp.ClientSession() as session:
        task1 = asyncio.create_task(poller(session))
        task2 = asyncio.create_task(scraper(session, update))
        task3 = asyncio.create_task(check_update(session))
        await task1
        await task2
        await task3


if __name__ == "__main__":
    db.init_tables()
    asyncio.run(main())
