import asyncio
from bs4 import BeautifulSoup
import db
import logging as log


URL = "https://vc.ru/popular"


def parsing(source):
    soup = BeautifulSoup(source, 'lxml')
    big_div = soup.find(attrs={"data-gtm": "Feed — Item 1 — Click"})
    if big_div:
        link = big_div.find(name="a", class_="content-link").get('href')
        return link


async def scraper(session, time):
    async with session.get(URL) as resp:
        while True:
            log.info("Run parser")
            response = parsing(await resp.text())
            last_url = db.get_last()
            if last_url != response:
                log.info(f"Get new url {response}")
                db.insert_url(response)
            log.info(f"Parser is sleeping for {time*60}")
            await asyncio.sleep(time * 60)
