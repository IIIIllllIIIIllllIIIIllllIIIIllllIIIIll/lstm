import sqlite3

conn = sqlite3.connect('cards.db')
c = conn.cursor()

for row in c.execute('SELECT * FROM cards WHERE is_new = 1 LIMIT 1'):
    print(row)
