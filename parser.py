import asyncio
import aiohttp
from bs4 import BeautifulSoup
URL = "https://vc.ru/popular"


def parsing(source):
    soup = BeautifulSoup(source, 'lxml')
    big_div = soup.find(attrs={"data-gtm": "Feed — Item 1 — Click"})
    if big_div:
        link = big_div.find(name="a", class_="content-link")
        print(link.get('href'))


async def scraper():
    async with aiohttp.ClientSession() as session:
        async with session.get(URL) as resp:
            response = await resp.text()
            parsing(response)

if __name__ == "__main__":
    asyncio.run(scraper())
