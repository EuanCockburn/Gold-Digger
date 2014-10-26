from yieldgenerator import *
from cuegenerator import *
from mine import *


class MineFactory():

    """Mine factory to create a mine of a specified depth. Creates a mine object, adds
     the correct number of blocks, and then generates yields and cues to be added to the
     blocks of the mine.

    :return: Mine"""

    def __init__(self, depth):
        self.depth = depth

    def make_mine(self, yield_generator, cue_generator):

        new_mine = Mine(0)

        for i in range(0, self.depth):
            new_mine.add_block(i)

        #yield_list = yield_generator(self.depth, 50, 0).get_yield()
        yield_list = [23, 18, 4, 7, 11, 9, 2, 3, 1, 0]
        new_mine.set_yields(yield_list)

        #cue_list = cue_generator(yield_list).make_cue()
        cue_list = [3, 2, 9, 4, 5, 2, 8, 9, 3, 7]
        new_mine.set_cues(cue_list)

        return new_mine

    def return_mine(self):
        pass