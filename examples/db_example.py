import sqlite3
import psycopg2
from sqlalchemy import create_engine

def access_db():
    # sqlite
    conn = sqlite3.connect(":memory:")
    cur = conn.cursor()
    cur.execute("CREATE TABLE t(id INTEGER, name TEXT)")
    cur.execute("INSERT INTO t VALUES(?, ?)", (1, "Alice"))
    conn.commit()
    print(cur.execute("SELECT * FROM t").fetchall())
    conn.close()

    # SQLAlchemy (just engine creation)
    eng = create_engine("sqlite:///:memory:")
    print("Engine:", eng)

if __name__ == "__main__":
    access_db()
