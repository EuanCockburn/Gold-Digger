from mine import *
from yieldgenerator import *
from cuegenerator import *

# class to receive a yield generator and a cue generator and use them to create a single mine


class MineFactory:

    def __init__(self, yield_generator, cue_generator):
        self.yield_generator = yield_generator
        self.cue_generator = cue_generator

    # creates a single mine using a yield and cue list to specify the available gold and cue displayed to the player at
    # each level of the mine
    def create_mine(self, depth, max_yield, scan_accuracy):
        yield_list = self.yield_generator.generate_array()
        cue_list = self.cue_generator.generate_array(yield_list)

        new_mine = Mine(depth)
        new_mine.populate_mine(yield_list, cue_list)

        return new_mine