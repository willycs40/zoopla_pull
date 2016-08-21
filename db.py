import MySQLdb
from parameters import Parameters
import logging

def run_sql(sql):
    db = MySQLdb.connect(host=Parameters.DB_HOST, user=Parameters.DB_USER, passwd=Parameters.DB_PASSWORD, db=Parameters.DB_SCHEMA)
    cursor = db.cursor()

    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()

    data = cursor.fetchall()
    db.close()

    try:
        return data[0][0]
    except:
        return True

def initialise_db():
    run_sql(Parameters.SQL_INITIALISE)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    initialise_db()