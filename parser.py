from bs4 import BeautifulSoup
from logger import log
import asyncio
import db

URL = "https://vc.ru/new"


def parser(source):
    soup = BeautifulSoup(source, 'lxml')
    big_div = soup.find(attrs={"data-gtm": "Feed — Item 1 — Click"})
    if big_div:
        link = big_div.find(name="a", class_="content-link").get('href')
        return link
    log.warning("Url not found")


async def last_link_from_url(session):
    async with session.get(URL) as resp:
        response = await resp.text()
        return str(parser(response))


async def check_for_updates(session, time):
    while True:
        link_from_site = await last_link_from_url(session)
        if link_from_site != db.get_last_link():
            log.info("New link")
            db.insert_url_into_db(link_from_site)
        else:
            log.info("Nothing new")
        await asyncio.sleep(time * 60)


if __name__ == "__main__":
    import aiohttp

    async def test():
        async with aiohttp.ClientSession() as session:
            await check_for_updates(session, 0.1)

    asyncio.run(test())
