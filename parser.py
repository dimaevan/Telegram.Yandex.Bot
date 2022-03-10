from bs4 import BeautifulSoup
import logging as log
import asyncio
import db


URL = "https://vc.ru/popular"


def search_last_link(source):
    soup = BeautifulSoup(source, 'lxml')
    big_div = soup.find(attrs={"data-gtm": "Feed — Item 1 — Click"})
    if big_div:
        link = big_div.find(name="a", class_="content-link").get('href')
        return link
    log.warning("Url not found")


async def scraper(session, time):
    async with session.get(URL) as resp:
        while True:
            response = search_last_link(await resp.text())
            last_url = db.get_last_url()
            if last_url != response:
                db.insert_url_into_db(response)
                log.info(f"Get new url {response}")
            log.info(f"No new links,"
                     f" parser is sleeping for {time} minutes")
            await asyncio.sleep(time * 1)
