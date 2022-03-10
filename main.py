from dataclasses import dataclass
from config import data_config
from collections import deque
from parser import check_for_updates
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
    text: str
    chat_id: int
    update_id: int

    def __repr__(self):
        return str(f"{self.text} {self.update_id}")


def build_query(method, host_url=host, token=my_config["bot"]["token"]):
    return f"{host_url}/bot{token}/{method}"


def parsing(data: list) -> None:
    for element in data:
        if element.get("my_chat_member"):
            key = 'my_chat_member'
        else:
            key = "message"
        x = Update(chat_id=element[key]['chat']['id'],
                   text=element[key].get('text'),
                   update_id=element['update_id'],
                   )
        updates.append(x)


async def init(session):
    url = build_query("getMe")
    async with session.get(url) as resp:
        response = await resp.json()
        if response['ok'] is True:
            log.info('Bot is ok!')


async def answer(text, chat_id, session):
    url = build_query("sendMessage")
    params = {"chat_id": chat_id}
    last_news_link = db.get_last_link()

    if text:
        db.insert_chat_into_db(chat_id)
        if text == "/start":
            params.update({"text": words.get(text)})
            await session.get(url, params=params)
            params.update({"text": f"Лови последнюю новость: {last_news_link}"})
            await session.get(url, params=params)
        elif text.startswith("/last"):
            params.update({"text": f"{last_news_link}"})
            await session.get(url, params=params)
        else:
            params.update({"text": text})
            await session.get(url, params=params)

        log.info(f"Answer to chat: {chat_id} ")


async def poller(session):
    offset = 0
    log.info("Starting poller")
    url = build_query("getUpdates")
    while True:
        params = {"offset": offset}
        async with session.get(url, params=params) as resp:
            response = await resp.json()
        if response.get("ok"):
            parsing(response.get("result"))
        if updates:
            offset = updates[-1].update_id + 1
            event: Update = updates.popleft()
            asyncio.create_task(answer(event.text, event.chat_id, session))
        await asyncio.sleep(1)


async def distribution(session, time):
    while True:
        links = db.get_last_not_sent_urls()
        if links:
            log.info(f"Start distribution, new links are {links}")
            chats = db.get_chats()
            for link in links:
                url = link[0]
                for chat in chats:
                    await answer(url, chat, session)
                log.info(f"New url send to {len(chats)} chats")
                db.change_status_link(str(url))
        await asyncio.sleep(time * 60)


async def main(update=1):
    async with aiohttp.ClientSession() as session:
        await init(session)
        await asyncio.gather(poller(session), check_for_updates(session, update), distribution(session, update))


if __name__ == "__main__":
    db.init_tables()
    asyncio.run(main())
