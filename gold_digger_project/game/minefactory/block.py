
class Block(object):

    """Creates a block object with a gold yield and a cue, which has a position in a Mine
    object and is either dug or not.

    :return: none"""

    def __init__(self, position):
        self.gold_yield = 0
        self.cue = 0
        self.dug = False
        self.position = position

    def set_cue(self, cue):
        self.cue = cue

    def set_yield(self, gold_yield):
        self.gold_yield = gold_yield

    def __str__(self):
        return 'Block pos: {pos},   gold: {gold},   cue: {cue},    dug: {dug}'.format\
            (pos=self.position, gold=self.gold_yield, cue=self.cue, dug=self.dug)