import sqlite3
conn = sqlite3.connect('database.db')
print "database opened successfully"
conn.execute('CREATE TABLE IF NOT EXISTS users(name TEXT,roll_no TEXT,branch TEXT,year TEXT,semester TEXT,email TEXT,mobile TEXT,password TEXT)')
conn.execute('CREATE TABLE IF NOT EXISTS profs(name TEXT,branch TEXT,semester TEXT)')
print "table created successfully"
conn.close()
