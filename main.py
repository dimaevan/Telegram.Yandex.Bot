import asyncio
import aiohttp
import pprint
from config import data_config
from dataclasses import dataclass
from datetime import datetime

my_config = data_config()
host = "https://api.telegram.org"


@dataclass
class Update:
    from_id: int
    chat: int
    date: int
    text: str

    def __repr__(self):
        return datetime.fromtimestamp(self.date).strftime("%d %B %Y %I:%M:%S")


updates = []


def build_query(method, host_url=host, token=my_config["token"]):
    return host_url + "/bot" + token + "/" + method


def pars(data: dict) -> None:
    if data["result"]:
        for message in data["result"]:
            x = Update(from_id=message['message']["from"]["id"],
                       chat=message['message']['chat']['id'],
                       date=message['message']['date'],
                       text=message['message']['text'],
                       )
            if x not in updates:
                updates.append(x)
        print(updates)


async def main():
    async with aiohttp.ClientSession() as session:
        url = build_query("getMe")

        async with session.get(url) as resp:
            response = await resp.json()
            pprint.pprint(response)


async def poller():
    async with aiohttp.ClientSession() as session:
        url = build_query("getUpdates?timeout=15")
        print(url)
        while True:
            async with session.get(url) as resp:
                response = await resp.json()
                pars(response)
            await asyncio.sleep(10)


async def answer():
    async with aiohttp.ClientSession() as session:

        url = build_query("sendMessage?timeout=15")
        print(url)
        while True:
            async with session.get(url) as resp:
                response = await resp.json()
                pprint.pprint(response)
            await asyncio.sleep(10)


if __name__ == "__main__":
    asyncio.run(poller())
