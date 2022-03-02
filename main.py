import asyncio
import aiohttp
import pprint
from config import data_config
from dataclasses import dataclass
from utils import format_date

my_config = data_config()
host = "https://api.telegram.org"


@dataclass
class Update:
    from_id: int
    chat: int
    date: int
    text: str
    update_id: int

    def __repr__(self):
        return str(f"{format_date(self.date)} {self.text} {self.update_id}")


updates = []


def build_query(method, host_url=host, token=my_config["bot"]["token"]):
    return host_url + "/bot" + token + "/" + method


def pars(data: dict) -> None:
    last_id = 0
    if data["result"]:
        for message in data["result"]:
            x = Update(from_id=message['message']["from"]["id"],
                       chat=message['message']['chat']['id'],
                       date=message['message']['date'],
                       text=message['message']['text'],
                       update_id=message['update_id']
                       )
            if x not in updates:
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


async def poller():
    print('Start poller')
    async with aiohttp.ClientSession() as session:
        off = 0
        while True:
            url = build_query(f"getUpdates?offset={off}")
            async with session.get(url) as resp:
                response = await resp.json()
            if response["result"]:
                off = pars(response) + 1
                print(updates)
            await asyncio.sleep(10)


async def answer():
    print('Start answer')
    async with aiohttp.ClientSession() as session:
        text = "Hello!"

        while True:
            if updates:
                for x in updates:
                    chat_id = x.chat
                    updates.remove(x)
                    url = build_query(f"sendMessage?chat_id={chat_id}&text={text}")
                    async with session.get(url) as resp:
                        response = await resp.json()
                        pprint.pprint(response)


async def main():
    await asyncio.gather(poller(), answer())


if __name__ == "__main__":
    asyncio.run(init())
    asyncio.run(main())
