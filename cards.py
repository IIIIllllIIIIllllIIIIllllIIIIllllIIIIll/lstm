import sqlite3
import uuid

conn = sqlite3.connect('cards.db')
c = conn.cursor()

with open("init.sql") as f:
    c.execute(f.read())

conn.commit()
conn.close()

def add_card(front, back):
    conn = sqlite3.connect('cards.db')
    c = conn.cursor()
    c.execute("INSERT INTO cards VALUES(?,?,?,?,?,?,?,?,?)", (
        str(uuid.uuid4()), 0, None, True, 4, None, None, front, back))
    conn.commit()
    conn.close()

def populate():
    add_card("J'ai mis des fleurs dans le vase.", "I placed flowers in the vase")
    add_card("Mon professeur met la barre haut.", "My teacher sets high standards.")

def get_training_s0_card():
    conn = sqlite3.connect('cards.db')
    c = conn.cursor()
    return list(c.execute('SELECT * FROM cards WHERE training_mode = 1 AND stage = 0 LIMIT 1'))
    conn.close()

def get_review():
    new = get_training_s0_card()
    if new:
        new = new[0]
        return {
            'new': True,
            'uuid': new[0],
            'front': new[7],
            'back': new[8]
        }

def do_review(card_id, ease):
    pass
