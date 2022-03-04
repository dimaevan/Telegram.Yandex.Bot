from dataclasses import dataclass
from config import data_config
from collections import deque
from parser import scraper
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


def pars(data: dict) -> int:
    last_id = 0
    if data["result"]:
        for message in data["result"]:
            x = Update(from_id=message['message']["from"]["id"],
                       chat_id=message['message']['chat']['id'],
                       date=message['message']['date'],
                       text=message['message']['text'],
                       update_id=message['update_id'],
                       message_id=message['message']['message_id'],
                       )
            updates.append(x)
            last_id = x.update_id
    return last_id


async def init():
    async with aiohttp.ClientSession() as session:
        url = build_query("getMe")
        async with session.get(url) as resp:
            response = await resp.json()
            if response['ok'] is True:
                print('Bot is ok!')


async def answer(text, chat_id):
    print('Start answer')
    async with aiohttp.ClientSession() as session:
        url = build_query("sendMessage")
        params = {"chat_id": chat_id, "text": text}
        await session.get(url, params=params)


async def poller(offset=0):
    async with aiohttp.ClientSession() as session:
        while True:
            print('Polling')
            url = build_query("getUpdates")
            params = {"offset": offset}
            async with session.get(url, params=params) as resp:
                response = await resp.json()
            if response.get("result"):
                offset = pars(response) + 1
            if updates:
                x: Update = updates.popleft()
                last_news_link = db.get_last()
                if x.text == "/start":
                    db.insert_chat(x.chat_id)
                    await answer(words.get("/start"), x.chat_id)
                    await answer(f"Лови {last_news_link}", x.chat_id)
                if x.text == "/last":
                    await answer(f"Лови {last_news_link}", x.chat_id)


async def check_update():
    last_link_id = db.get_last()
    while True:
        print("Check update")
        new_link_id, url = await db.get_last()
        if last_link_id is not new_link_id:
            chats = db.get_chats()
            for chat in chats:
                await answer(f"Лови {url}", chat)
            db.update_link()
        else:
            print("No update")
        await asyncio.sleep(10)


async def main(update=1):
    db.init_tables()
    await init()
    task1 = asyncio.create_task(poller())
    task2 = asyncio.create_task(scraper(update))
    task3 = asyncio.create_task(check_update())
    await task1
    await task2
    await task3


if __name__ == "__main__":
    asyncio.run(main())
