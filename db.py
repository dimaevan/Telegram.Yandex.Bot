import psycopg2
import config
# TODO  INSERT HTML
conf = config.data_config()["database"]


def access_db(query):
    try:
        connection = psycopg2.connect(**conf)
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        cursor.close()
    except psycopg2.Error as e:
        print(f"Warning: {e}")
    finally:
        psycopg2.connect().close()


def init():
    query_init = "CREATE TABLE IF NOT EXISTS links (id serial PRIMARY KEY , url TEXT, time INT UNIQUE, posted boolean);"
    access_db(query_init)


def insert(url, date):
    query = f"INSERT INTO links (url, time, posted) VALUES ('{url}',{date},{False});"
    access_db(query)


if __name__ == "__main__":

    init()
    insert('https://vc.ru/offline/372275-nuzhno-zakanchivat-ves-etot-goskapitalizm-deripaska-fridman-i-tinkov-vyskazalis-protiv-voyny-na-ukraine', 1646052970)
