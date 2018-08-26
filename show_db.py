import datetime
import time
import sqlite3
from tabulate import tabulate
from decimal import Decimal

HEADERS = [
    "uuid",
    "stage",
    "due",
    "type",
    "ease",
    "last",
    "front",
    "back",
]

conn = sqlite3.connect('cards.db')
c = conn.cursor()

rows = list(c.execute('SELECT * FROM cards'))

def compress(row):

    def trunc(s):
        if not isinstance(s, str): return s
        if len(s) >= 15:
            return s[0:15] + ".."
        return s

    def delta_from_time(t):
        if t is None: return t
        if isinstance(t, str):
            t = int(t)
        dtime_secs = t - time.time()
        return round(Decimal(dtime_secs / 86400), 2)

    uuid, stage, due, card_type, ease, last, front, back = row

    return (uuid.split('-')[0], stage, delta_from_time(due), ['TRAINING', 'LAPSED', 'REGULAR'][card_type], ease, delta_from_time(last), trunc(front), trunc(back))

rows = [compress(row) for row in rows]

print(tabulate(
    rows,
    headers=HEADERS
))
