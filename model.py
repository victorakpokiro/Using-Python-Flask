
import records 
from contextlib import contextmanager

@contextmanager
def db_conn_mgr():
    con = "sqlite:///applocalStorage.db"
    db = records.Database(con, echo=True)

    conn = db.get_connection()
    cur = conn.transaction()
    try:
        yield conn
        cur.commit()
    except Exception as e:
        cur.rollback()
        raise e 

    finally:
        cur.close()




def create_table(sqlfile):

    with db_conn_mgr() as db:
        db.query(sqlfile)

