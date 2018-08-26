import time
import sqlite3
import uuid

import asm2

SECONDS_IN_A_DAY = 86400

conn = sqlite3.connect('cards.db')
c = conn.cursor()

with open("init.sql") as f:
    c.execute(f.read())

conn.commit()
conn.close()

def add_card(front, back):
    conn = sqlite3.connect('cards.db')
    c = conn.cursor()
    c.execute("INSERT INTO cards VALUES(?,?,?,?,?,?,?,?)", (
        str(uuid.uuid4()), 0, None, 0, None, None, front, back))
    conn.commit()
    conn.close()

def select(*args):
    conn = sqlite3.connect('cards.db')
    c = conn.cursor()
    ret = list(c.execute(*args))
    conn.close()
    return ret

def execute(*args):
    conn = sqlite3.connect('cards.db')
    c = conn.cursor()
    c.execute(*args)
    conn.commit()
    conn.close()

def get_training_s0_card():
    return select('SELECT * FROM cards WHERE type = 0 AND stage = 0 LIMIT 1')

def get_training_s1_card():
    return select('SELECT * FROM cards WHERE type = 0 AND stage = 1 LIMIT 1')

def get_lapsed_cards():
    return select('SELECT * FROM cards WHERE type = 1 LIMIT 1')

# get the next rep
def get_review():
    new = get_training_s0_card()
    if new:
        new = new[0]
        return {
            'uuid': new[0],
            'type': new[3],
            'front': new[6],
            'back': new[7],
            'hypothetical_next_dues': [
                '<1m', None, '<10m', '4d'
            ]
        }
    new = get_training_s1_card()
    if new:
        new = new[0]
        return {
            'uuid': new[0],
            'type': new[3],
            'front': new[6],
            'back': new[7],
            'hypothetical_next_dues': [
                '<1m', None, '1d', '4d'
            ]
        }
def get_card_by_id(card_id):
    l = select("SELECT * FROM cards WHERE uuid=?", (card_id,))
    if len(l) == 0:
        return None
    assert len(l) == 1
    return l[0]

def post_card_of(card, ease):
    card_type = card[3]
    if card_type == 0:
        return post_card_of_review(card, ease)
    else:
        raise Exception("unimplemented")

def post_card_of_review(card, ease):
    tck_pre = asm2.TrainingCardKnowledge(
        stage = card[1],
    )
    return asm2.updateOnReview(
        ck = tck_pre,
        score = ease
    )

def do_rep(card_id, ease):
    card = get_card_by_id(card_id)
    post_card = post_card_of(card, ease)
    if isinstance(post_card, asm2.TrainingCardKnowledge):
        execute("UPDATE cards SET stage=? WHERE uuid=?", (
            post_card.stage,
            card[0],
        ))
    elif isinstance(post_card, asm2.CardKnowledge):
        assert post_card.last == 0

        execute("UPDATE cards SET stage=NULL, type=?, ease=?, due=?, last=? WHERE uuid=?", (
            2,
            post_card.ease,
            int(time.time()) + post_card.due * SECONDS_IN_A_DAY,
            int(time.time()),
            card[0],
        ))
        print('executed', card[0])

    else:
        raise Exception("unimplemented")
