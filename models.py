import sqlite3


def drop_table():
    with sqlite3.connect('reddit.db') as connection:
        c = connection.cursor()
        c.execute("""DROP TABLE IF EXISTS posts;""")
    return True

def drop_table2():
    with sqlite3.connect('reddit.db') as connection:
        c = connection.cursor()
        c.execute("""DROP TABLE IF EXISTS comments;""")
    return True

def drop_table3():
    with sqlite3.connect('reddit.db') as connection:
        c = connection.cursor()
        c.execute("""DROP TABLE IF EXISTS users;""")
    return True

def create_db():
    with sqlite3.connect('reddit.db') as connection:
        c = connection.cursor()
        table = """CREATE TABLE posts(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            body TEXT NOT NULL,
            author TEXT NOT NULL,
            image_url TEXT NOT NULL,
            vote_count INTEGER NOT NULL DEFAULT 0,
            created_at DATE DEFAULT CURRENT_TIMESTAMP NOT NULL
        );
        """
        c.execute(table)
    return True

def create_db2():
        with sqlite3.connect('reddit.db') as connection:
            c = connection.cursor()
            table = """CREATE TABLE comments(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                author TEXT NOT NULL,
                created_at DATE DEFAULT CURRENT_TIMESTAMP NOT NULL,
                post_id INTEGER,
                FOREIGN KEY(post_id) REFERENCES posts(id)
            );
            """
            c.execute(table)
        return True

def create_db3():
        with sqlite3.connect('reddit.db') as connection:
            c = connection.cursor()
            table = """CREATE TABLE users(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                created_at DATE DEFAULT CURRENT_TIMESTAMP NOT NULL
            );
            """
            c.execute(table)
        return True


if __name__ == '__main__':
    drop_table()
    drop_table2()
    drop_table3()
    create_db()
    create_db2()
    create_db3()
