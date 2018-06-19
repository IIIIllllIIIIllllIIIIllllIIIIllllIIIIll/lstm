import sqlite3

conn = sqlite3.connect('cards.db')
c = conn.cursor()

for row in c.execute('SELECT * FROM cards'):
    print(row)
