from enum import Enum


class Action(Enum):

    COOPERATE = 1
    DEFECT = 2


class Persuasion(Enum):

    TRUTH = 1
    LIE = 2


class Belief(Enum):

    BELIEVE = 1
    DOUBT = 2
