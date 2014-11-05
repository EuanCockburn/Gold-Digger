# class to represent a single diggable entity within a mine object


class Block:

    # initialise the instance by setting yield and cue
    def __init__(self, gold_yield, gold_cue):
        self.gold_yield = gold_yield
        self.gold_cue = gold_cue

    # Getters for the block instance's yield and cue
    def get_yield(self):
        return self.gold_yield

    def get_cue(self):
        return self.gold_cue