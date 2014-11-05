from block import *

# class to represent a single mine composed of multiple diggable blocks


class Mine:

    def __init__(self, depth):
        self.depth = depth
        self.block_position = 0
        self.block_list = []

    # function to populate the mine with blocks that each have a certain yield and cue displayed to the player
    def populate_mine(self, yield_list, cue_list):
        for i in range(self.depth):
            gold_yield = yield_list[i]
            gold_cue = cue_list[i]
            new_block = Block(gold_yield, gold_cue)
            self.block_list.append(new_block)

    # function to check if the player has reached the bottom of the mine
    def mine_exhausted(self):
        if self.block_position == self.depth - 1:
            return True
        else:
            return False

    # function to return the current block position
    def get_block_position(self):
        return self.block_position

    # function to return the current block
    def get_current_block(self):
        return self.block_list[self.block_position]

    # function to return the next block in the mine
    def get_next_block(self):
        self.block_position += 1
        return self.block_list[self.block_position]