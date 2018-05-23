import sqlite3

conn = sqlite3.connect('cards.db')
c = conn.cursor()

with open("init.sql") as f:
    c.execute(f.read())

conn.commit()
conn.close()

def add_card(front, back):
    conn = sqlite3.connect('cards.db')
    c = conn.cursor()
    c.execute("INSERT INTO cards VALUES(?,?,?,?,?,?,?)", (None, True, 4, None, None, front, back))
    conn.commit()
    conn.close()

def populate():
    add_card("J'ai mis des fleurs dans le vase.", "I placed flowers in the vase")
    add_card("Mon professeur met la barre haut.", "My teacher sets high standards.")

def get_new_card():
    conn = sqlite3.connect('cards.db')
    c = conn.cursor()
    return list(c.execute('SELECT * FROM cards WHERE is_new = 1 LIMIT 1'))
    conn.close()
