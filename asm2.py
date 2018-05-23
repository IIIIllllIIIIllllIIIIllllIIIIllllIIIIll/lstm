#!/usr/bin/env python3

from dataclasses import dataclass

@dataclass
class TrainingCardKnowledge(object):
    stage: int
    graduating_interval: int

@dataclass
class CardKnowledge(object):
    ease: int
    last: int
    due: int

AGAIN = 0
HARD = 1
GOOD = 2
EASY = 3

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

def updateOnReview(ck, score):

    # red to red
    if isinstance(ck, TrainingCardKnowledge) and score == AGAIN:
        return TrainingCardKnowledge(
            stage = 0,
            graduating_interval = ck.graduating_interval
        )
    if isinstance(ck, TrainingCardKnowledge) and score == GOOD:
        if ck.stage == 0:
                return TrainingCardKnowledge(
                stage = 1,
                graduating_interval = ck.graduating_interval
            )
        else:
            return graduate(ck)
    if isinstance(ck, TrainingCardKnowledge) and score == EASY:
        return graduate(now, ck)

    interval = -ck.last

    # orange to red
    if isinstance(ck, CardKnowledge) and score == AGAIN :
        return TrainingCardKnowledge(
            stage = 1,
            graduating_interval = 1
        )

    # orange to orange
    if isinstance(ck, CardKnowledge) and score == HARD:
        return schedule_next(ck.ease - 20, interval * 1.2)
    if isinstance(ck, CardKnowledge) and score == GOOD:
        return schedule_next(ck.ease, interval * ck.ease/100)
    if isinstance(ck, CardKnowledge) and score == EASY:
        return schedule_next(ck.ease, interval * ck.ease/100 * 1.3)

# entry point

def newCard():
    return TrainingCardKnowledge(
        stage = 0,
        graduating_interval = 4
    )
