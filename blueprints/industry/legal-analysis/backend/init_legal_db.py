import sqlite3

connection = sqlite3.connect('database/legal_data.db')

with open('database/schema.sql') as f:
    connection.executescript(f.read())

connection.commit()
connection.close()
