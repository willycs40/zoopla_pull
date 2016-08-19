import MySQLdb
db = MySQLdb.connect(host="mysql", user="will", passwd="housepass", db="housing")
cursor = db.cursor()

#cursor.execute("SELECT name, phone_number FROM coworkers WHERE name=%s AND clue > %s LIMIT 5", (name, clue_threshold))
cursor.execute("select * from test")

data = cursor.fetchall()
for row in data :
    print(row)

db.close()


