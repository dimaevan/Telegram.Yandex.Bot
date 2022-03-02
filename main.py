import asyncio
import pprint
import aiohttp
from config import data_config
from dataclasses import dataclass
from utils import format_date
from parser import scraper
import sys

my_config = data_config()
host = "https://api.telegram.org"


@dataclass
class Update:
    from_id: int
    date: int
    text: str
    chat_id: int
    update_id: int
    message_id: int

    def __repr__(self):
        return str(f"{format_date(self.date)} {self.text} {self.update_id}")

#TODO add queue
updates = []


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


async def answer():
    sys.stdout.write('\rStart answer')
    async with aiohttp.ClientSession() as session:
        text = "Hello!"
        if updates:
            for x in updates:
                updates.remove(x)
                url = build_query("sendMessage")
                params = {"chat_id": x.chat_id, "text": text,
                          "message_id": x.message_id}
                await session.get(url, params=params)


async def poller(offset=0):
    async with aiohttp.ClientSession() as session:
        while True:
            sys.stdout.write('\rPolling')
            url = build_query("getUpdates")
            params = {"offset": offset}
            async with session.get(url, params=params) as resp:
                response = await resp.json()
            if response["result"]:
                offset = pars(response) + 1
            if updates:
                await answer()


async def main():
    await init()
    task1 = asyncio.create_task(poller())
    task2 = asyncio.create_task(scraper())
    await task1
    await task2


if __name__ == "__main__":
    asyncio.run(main())
