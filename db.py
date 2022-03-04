import psycopg2
import config


conf = config.data_config()["database"]


def access_db(query, commit=False):
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
        print('already exists')
    except psycopg2.Error as e:
        print(f"Warning: {e}")
    finally:
        psycopg2.connect().close()


def init_tables():
    query_init = """CREATE TABLE IF NOT EXISTS link
     (link_id serial PRIMARY KEY , url TEXT UNIQUE);"""
    access_db(query_init, True)
    query_init = """
    CREATE TABLE IF NOT EXISTS chat
    (id serial PRIMARY KEY, chat_id bigint UNIQUE, link_id serial );
    """
    access_db(query_init, True)


def insert_url(url):
    query = f"INSERT INTO link (url) VALUES ('{url}');"
    access_db(query, True)


def insert_chat(chat_id):
    query = f"""INSERT INTO chat (chat_id,link_id)
     VALUES ('{chat_id}', (SELECT max(link_id) FROM link ) );
    """
    access_db(query, True)


def get_last():
    query = """SELECT url FROM link ORDER BY link_id DESC LIMIT 1; """
    if access_db(query):
        return access_db(query)[0][0]


def get_chats():
    query = """SELECT chat_id FROM chat; """
    chats = access_db(query, False)
    return [x[0] for x in chats]


def update_link():
    query = """UPDATE chat SET link_id=(SELECT max(link_id) FROM link);"""
    access_db(query, True)


def truncate_tables():
    query = """TRUNCATE chat"""
    access_db(query, True)
    query = """TRUNCATE link"""
    access_db(query, True)


if __name__ == "__main__":
    print(get_last())
