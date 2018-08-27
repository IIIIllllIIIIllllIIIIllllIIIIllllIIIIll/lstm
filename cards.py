import time
import sqlite3
import uuid
import math

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

def get_regular_due_cards():
    return select('SELECT * FROM cards WHERE type = 2 AND due < ? LIMIT 1', (str(int(time.time())),))

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
    # new = get_lapsed_cards()
    new = get_regular_due_cards()
    if new:
        new = new[0]
        ret = {
            'uuid': new[0],
            'type': new[3],
            'front': new[6],
            'back': new[7],
            'hypothetical_next_dues': [
                '?', '?', '?', '?'
            ]
        }
        for ease in range(4):
            print("ease=", ease, post_card_of(new, ease))

        return ret

def get_card_by_id(card_id):
    l = select("SELECT * FROM cards WHERE uuid=?", (card_id,))
    if len(l) == 0:
        return None
    assert len(l) == 1
    return l[0]

def post_card_of(card, ease):
    card_type = card[3]
    if card_type == 0:
        return post_card_of_training(card, ease)
    elif card_type == 1:
        return post_card_of_lapsed(card, ease)
    elif card_type == 2:
        return post_card_of_regular(card, ease)
    else:
        raise Exception("unimplemented")

def post_card_of_training(card, ease):
    tck_pre = asm2.TrainingCardKnowledge(
        stage = card[1],
    )
    return asm2.updateOnReview(
        ck = tck_pre,
        score = ease
    )

def post_card_of_lapsed(card, ease):
    lck_pre = asm2.LapsedCardKnowledge(
        ease = card[4],
    )
    return asm2.updateOnReview(
        ck = lck_pre,
        score = ease
    )

def post_card_of_regular(card, ease):
    dtime_secs = int(card[5]) - time.time()
    dtime_days = math.ceil(dtime_secs / SECONDS_IN_A_DAY)
    rck_pre = asm2.CardKnowledge(
        ease = card[4],
        last = dtime_days,
        due = None,
    )
    return asm2.updateOnReview(
        ck = rck_pre,
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
        assert post_card.last == None

        execute("UPDATE cards SET stage=NULL, type=?, ease=?, due=?, last=? WHERE uuid=?", (
            2,
            post_card.ease,
            int(time.time() + post_card.due * SECONDS_IN_A_DAY),
            int(time.time()),
            card[0],
        ))
        print('executed', card[0])

    else:
        raise Exception("unimplemented")
