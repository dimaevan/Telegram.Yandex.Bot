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
            record = cursor.fetchone()
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
     (link_id serial PRIMARY KEY , url TEXT, time INT UNIQUE);"""
    access_db(query_init, True)
    query_init = """
    CREATE TABLE IF NOT EXISTS chat
    (id serial PRIMARY KEY, chat_id serial, link_id serial REFERENCES link );
    """
    access_db(query_init,True)


def insert_url(url, date):
    query = f"""INSERT INTO link (url, time)
     VALUES ('{url}',{date});"""
    access_db(query)


def insert_chat(chat_id):
    query = f"""INSERT INTO chat (chat_id,link_id)
     VALUES ('{chat_id}', (SELECT max(link_id) FROM link ) );
    """
    access_db(query)


def get_last():
    query = """SELECT link_id, url FROM link DESK LIMIT 1; """
    print(access_db(query))


if __name__ == "__main__":
    init_tables()
    get_last()

