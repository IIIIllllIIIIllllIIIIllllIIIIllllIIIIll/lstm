import sqlite3
from tabulate import tabulate

HEADERS = [
    "uuid",
    "stage",
    "due",
    "training_mode",
    "graduating_interval",
    "ease",
    "last",
    "front",
    "back",
]

conn = sqlite3.connect('cards.db')
c = conn.cursor()

print(tabulate(
    list(c.execute('SELECT * FROM cards')),
    headers=HEADERS
))
