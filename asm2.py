#!/usr/bin/env python3

# Anki-flavoured supermemo2 scheduling algorithm
# does not support early review

import math
from dataclasses import dataclass

@dataclass
class LapsedCardKnowledge(object):
    ease: int       # inherited from ease of parent card

@dataclass
class TrainingCardKnowledge(object):
    stage: int

@dataclass
class CardKnowledge(object):
    ease: int       # increases or decreases when not ranked GOOD
    last: int       # date of last review (negative for overdue)
    due: int        # date of next review

AGAIN = 0
HARD = 1
GOOD = 2
EASY = 3

class InvalidChoice(Exception):
    pass

def schedule_next(ease, due_in):
    return CardKnowledge(
        ease = ease,
        last = None,
        due = due_in,
    )

def updateTCKOnReview(ck, score):
    if score == AGAIN:
        return TrainingCardKnowledge(
            stage = 0,
        )
    if score == HARD:
        raise InvalidChoice()
    if score == GOOD:
        if ck.stage == 0:
            return TrainingCardKnowledge(
                stage = 1,
            )
        else:
            return schedule_next(
                ease = 250,
                due_in = 1
            )
    if score == EASY:
        return schedule_next(
            ease = 250,
            due_in = 4
        )

def updateCKOnReview(ck, score):
    interval = -ck.last

    assert(interval >= 0)

    # orange to red
    if isinstance(ck, CardKnowledge) and score == AGAIN :
        return LapsedCardKnowledge(
            ease = max(130, ck.ease - 20)
        )
    # orange to orange
    if isinstance(ck, CardKnowledge) and score == HARD:
        return schedule_next(max(130, ck.ease - 15), interval * 1.2)
    if isinstance(ck, CardKnowledge) and score == GOOD:
        return schedule_next(ck.ease, interval * ck.ease/100)
    if isinstance(ck, CardKnowledge) and score == EASY:
        return schedule_next(ck.ease + 15, interval * ck.ease/100 * 1.3)

def updateLKOnReview(ck, score):
    # todo: I think lapsed cards can only be marked "AGAIN" or
    # "GOOD"; confirm this
    if score == AGAIN:
        return ck
    if score == HARD:
        raise InvalidChoice()
    if score == GOOD:
        if ck.stage == 0:
            return schedule_next(ck.ease, 1)
        else:
            return schedule_next(
                ck.ease,
                due_in = 1
            )
    if score == EASY:
        raise InvalidChoice()

def updateOnReview(ck, score):
    if isinstance(ck, TrainingCardKnowledge):
        return updateTCKOnReview(ck, score)
    if isinstance(ck, CardKnowledge):
        return updateCKOnReview(ck, score)
    if isinstance(ck, LapsedCardKnowledge):
        return updateLKOnReview(ck, score)
    raise TypeError()

# entry point

def newCard():
    return TrainingCardKnowledge(
        stage = 0,
    )
