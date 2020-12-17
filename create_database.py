import sqlite3
from operator import itemgetter
conn = sqlite3.connect('database.db')

conn.execute('CREATE TABLE IF NOT EXISTS users(name TEXT,roll_no TEXT,branch TEXT,semester TEXT,email TEXT,mobile TEXT,password TEXT)')
conn.execute('CREATE TABLE IF NOT EXISTS profs(name TEXT,branch TEXT, subject TEXT,semester TEXT)')
conn.execute('CREATE TABLE IF NOT EXISTS feedback (lecturer TEXT, st_rollno TEXT, year TEXT, semester TEXT, branch TEXT, subject TEXT, preparation TEXT, information TEXT, explanation TEXT, pace TEXT, leadership TEXT, receptive TEXT, interest TEXT, discussion TEXT, learning TEXT, rapport TEXT, available TEXT )')
conn.commit()
# a=conn.execute('INSERT INTO profs (name,branch,subject,semester) VALUES("Jasleen", "ece", "Device Modulation", 5),("Pranshu", "ece", "Microprocessor", 5),("Sumit Singh", "ece", "Control Device", 5),("Guleriya", "ece", "Antenna", 5)')
# #x=conn.execute('select lecturer,avg(preparation),avg(information),avg(explanation),avg(pace),avg(leadership),avg(receptive),avg(interest),avg(discussion),avg(learning),avg(rapport),avg(available) from feedback group by lecturer')
# q=conn.execute('select avg(preparation),avg(information),avg(explanation),avg(pace),avg(leadership),avg(receptive),avg(interest),avg(discussion),avg(learning),avg(rapport),avg(available) from feedback where lecturer="Divyansh Thakur" and branch="cse" and semester="5"')
# conn.commit()

# conn.execute('delete from feedback')
# conn.commit()
q=conn.execute('select * from users')

l=q.fetchall()
print(l)


conn.close()
