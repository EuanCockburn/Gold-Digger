# class to represent a single diggable entity within a mine object


class Block:
    yield_hint = 0
    cue_hint = 0
    gold_yield = 0
    gold_cue = 0
    dug = False

    # initialise the instance by setting yield and cue
    def __init__(self, gold_yield, gold_cue, max_yield):
        self.yield_hint = (6 * gold_yield)/max_yield + 1
        self.cue_hint = (6 * gold_cue)/max_yield + 1
        self.gold_yield = gold_yield
        self.gold_cue = gold_cue
        self.dug = False

    # Getters for the block instance's yield and cue
    def get_yield(self):
        return self.gold_yield

    def get_cue(self):
        return self.gold_cue

    def dig(self):
        self.dug = True