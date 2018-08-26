import sqlite3
from tabulate import tabulate

HEADERS = [
    "uuid",
    "stage",
    "due",
    "type",
    "grad",
    "ease",
    "last",
    "front",
    "back",
]

conn = sqlite3.connect('cards.db')
c = conn.cursor()

rows = list(c.execute('SELECT * FROM cards'))

def compress_uuid(row):
    return tuple((row[0].split('-')[0],)) + tuple(col for col in row[1:])

rows = [compress_uuid(row) for row in rows]

print(tabulate(
    rows,
    headers=HEADERS
))
