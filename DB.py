import sqlite3

conn = sqlite3.connect('database.db')
print ("Opened database successfully")

conn.execute('CREATE TABLE arriver (id TEXT PRIMARY KEY,nom TEXT, temps_arrivee TEXT, temps_depart TEXT )')
print ("Table created successfully")
conn.close()