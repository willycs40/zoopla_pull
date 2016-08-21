import MySQLdb
from parameters import Parameters
import logging

def run_sql(sql, db=None):
    
    db = MySQLdb.connect(host=Parameters.DB_HOST, user=Parameters.DB_USER, passwd=Parameters.DB_PASSWORD, db=Parameters.DB_SCHEMA)    
    cursor = db.cursor()
    
    logging.debug(sql)
    
    try:
        cursor.execute(sql)
        db.commit()
        data = cursor.fetchall()
        db.close()
    except Exception as e:
        logging.error(e)
        db.rollback()
    try:
        return data[0][0]
    except:
        return True
        
def run_sql_multi(sql_list):
    for sql in sql_list:
        run_sql(sql)
           
def initialise_db():
    run_sql_multi(Parameters.SQL_INITIALISE)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    initialise_db()
