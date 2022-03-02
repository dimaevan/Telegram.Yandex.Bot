import asyncio
import aiohttp
from bs4 import BeautifulSoup
import db
URL = "https://vc.ru/popular"


def parsing(source):
    soup = BeautifulSoup(source, 'lxml')
    big_div = soup.find(attrs={"data-gtm": "Feed — Item 1 — Click"})
    if big_div:
        link = big_div.find(name="a", class_="content-link").get('href')
        date = big_div.find(attrs={"air-module": "module.entry"})\
            .get("data-publish-date")
        return link, int(date)


async def scraper():
    async with aiohttp.ClientSession() as session:
        async with session.get(URL) as resp:
            while True:
                response = await resp.text()
                db.insert_url(*parsing(response))
                await asyncio.sleep(60*60)

if __name__ == "__main__":
    asyncio.run(scraper())
