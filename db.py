import logging
import psycopg2
import config


conf = config.data_config()["database"]


def access_to_db(query, commit=True):
    try:
        connection = psycopg2.connect(**conf)
        cursor = connection.cursor()
        cursor.execute(query)
        if commit:
            connection.commit()
        else:
            record = cursor.fetchall()
            cursor.close()
            return record
    except psycopg2.IntegrityError:
        return False
    except psycopg2.Error as e:
        logging.info(f"Warning: {e}")
    finally:
        psycopg2.connect().close()


def init_tables():
    query_init = """CREATE TABLE IF NOT EXISTS link
     (link_id serial PRIMARY KEY , url TEXT UNIQUE,
      sent BOOLEAN DEFAULT False);"""
    access_to_db(query_init)
    query_init = """
    CREATE TABLE IF NOT EXISTS chat
    (id serial PRIMARY KEY, chat_id bigint UNIQUE );
    """
    access_to_db(query_init)


def insert_url_into_db(url) -> bool:
    query = f"INSERT INTO link (url) VALUES ('{url}');"
    access_to_db(query, True)
    return True


def insert_chat_into_db(chat_id) -> None:
    query = f"""INSERT INTO chat (chat_id) VALUES ('{chat_id}'); """
    access_to_db(query)


def get_last_link() -> str:
    """
    Return last url
    """
    query = """SELECT url FROM link ORDER BY link_id DESC LIMIT 1; """
    last = access_to_db(query, False)
    if last:
        return str(last[0][0])
    else:
        return ""


def get_last_not_sent_urls() -> list:
    """
    Return list links that not send
    """
    query = """SELECT url FROM link WHERE sent='f' """
    urls = access_to_db(query, False)
    return urls


def change_status_link(url) -> None:
    query = f"""UPDATE link SET sent='t' where url='{url}'"""
    access_to_db(query)


def get_chats() -> list:
    """
    Return array of id chat
    """
    query = """SELECT chat_id FROM chat; """
    chats = access_to_db(query, False)
    return [x[0] for x in chats]


if __name__ == "__main__":
    pass
