from block import *


class Mine():

    """Creates a mine object which is constructed of blocks. Also notes current position in
    block layers."""

    def __init__(self, current_position):
        self.current_position = current_position
        self.block_list = []

#Mutator methods for mine attributes including setting yields and cues of each mine block

    def add_block(self, pos):
        new_block = Block(pos)
        self.block_list.append(new_block)


    def set_yields(self, yield_list):
        i = 0
        for block in self.block_list:
            block.set_yield(yield_list[i])
            i += 1

    def set_cues(self, cue_list):
        i = 0
        for block in self.block_list:
            block.set_cue(cue_list[i])
            i += 1

    def set_position(self, pos):
        self.current_position = pos

#Accessor methods for mine attributes

    def get_block_list(self):
        return self.block_list

    def get_position(self):
        return self.current_position

    def __str__(self):
        #Overrides default string method
        string = ""
        for block in self.block_list:
            string += block.__str__() + "\n"
        return string