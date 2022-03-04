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
        # date = big_div.find(attrs={"air-module": "module.entry"})\
        #     .get("data-publish-date")
        return link


async def scraper(time):
    print("Run parser")
    async with aiohttp.ClientSession() as session:
        async with session.get(URL) as resp:
            while True:
                current_last_url = db.get_last()
                response = await resp.text()
                if current_last_url is not parsing(response):
                    print("Add new url!")
                    db.insert_url(parsing(response))
                print("Waiting")
                await asyncio.sleep(time * 60)

if __name__ == "__main__":
    asyncio.run(scraper(1))
