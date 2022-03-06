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
            log.info("Run parser")
            response = search_last_link(await resp.text())
            last_url = db.get_last_url()
            if last_url != response:
                if db.insert_url_into_db(response):
                    log.info(f"Get new url {response}")
            else:
                log.info("No new links :c")
            log.info(f"Parser is sleeping for {time*60}")
            await asyncio.sleep(time * 60)
