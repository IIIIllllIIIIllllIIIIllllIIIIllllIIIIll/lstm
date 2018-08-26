#!/usr/bin/env python3

# Anki-flavoured supermemo2 scheduling algorithm
# does not support early review

from dataclasses import dataclass

@dataclass
class LapsedCardKnowledge(object):
    ease: int       # inherited from ease of parent card

@dataclass
class TrainingCardKnowledge(object):
    stage: int
    graduating_interval: int

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

def schedule_next(ease, interval_to_next):
    return CardKnowledge(
        ease = ease,
        last = 0,
        due = interval_to_next,
    )

def graduate(ck):
    if isinstance(ck, TrainingCardKnowledge):
        ease = 250
    else:
        ease = ck.ease
    return schedule_next(ease, ck.graduating_interval)

def updateTCKOnReview(ck, score):
    if score == AGAIN:
        return TrainingCardKnowledge(
            stage = 0,
            graduating_interval = ck.graduating_interval
        )
    if score == HARD:
        raise InvalidChoice()
    if score == GOOD:
        if ck.stage == 0:
            return TrainingCardKnowledge(
                stage = 1,
                graduating_interval = ck.graduating_interval
            )
        else:
            return graduate(ck)
    if score == EASY:
        return graduate(ck)

def updateCKOnReview(ck, score):
    interval = -ck.last

    assert(interval >= 0)

    # orange to red
    if isinstance(ck, CardKnowledge) and score == AGAIN :
        return LapsedCardKnowledge(
            ease = ck.ease
        )
    # orange to orange
    if isinstance(ck, CardKnowledge) and score == HARD:
        return schedule_next(ck.ease - 20, interval * 1.2)
    if isinstance(ck, CardKnowledge) and score == GOOD:
        return schedule_next(ck.ease, interval * ck.ease/100)
    if isinstance(ck, CardKnowledge) and score == EASY:
        return schedule_next(ck.ease, interval * ck.ease/100 * 1.3)

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
            return graduate(ck)
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
        graduating_interval = 4
    )
