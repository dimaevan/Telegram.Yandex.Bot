import sqlite3

# TODO  INSERT HTML


def access_db(query):
    try:
        sqlite_conn = sqlite3.connect("db.db")
        cursor = sqlite_conn.cursor()
        cursor.execute(query)
        record = cursor.fetchall()
        cursor.close()
        return record
    except sqlite3.Error as e:
        print(f"Warning: {e}")


def init():
    query_init = "CREATE TABLE IF NOT EXISTS links (id INT PRIMARY KEY, url TEXT(500), time DATE, posted INT);"
    response = access_db(query_init)
    return response


def insert(url, date):
    query = f"INSERT INTO links (url, time , posted) VALUES ({url},{date},{0});"
    print(query)
    access_db(query)


if __name__ == "__main__":
    init()
