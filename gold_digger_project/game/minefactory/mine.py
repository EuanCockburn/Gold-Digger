from block import *

# class to represent a single mine composed of multiple diggable blocks


class Mine:

    def __init__(self, depth):
        self.depth = depth
        self.block_position = 0
        self.block_list = []
        self.optimal = -1

    # function to populate the mine with blocks that each have a certain yield and cue displayed to the player
    def populate_mine(self, yield_list, cue_list, dig, move):
        for i in range(self.depth):
            gold_yield = yield_list[i]
            gold_cue = cue_list[i]
            new_block = Block(gold_yield, gold_cue)
            self.block_list.append(new_block)
        self.optimal = self.calculate_optimal(yield_list, dig, move)

    # function to check if the player has reached the bottom of the mine
    def mine_exhausted(self):
        if self.block_position == self.depth:
            return 1
        return 0

    # function to return the current block position
    def get_block_position(self):
        return self.block_position

    # function advance the players position within the mine
    def inc_block_pos(self):
        self.block_position += 1

    # function to return the current block
    def get_current_block(self):
        return self.block_list[self.block_position]

    # function to return the optimal stop point
    def get_optimal(self):
        return self.optimal

    # function to calculate the optimal stopping point of a mine
    @staticmethod
    def calculate_optimal(yield_array, dig_cost, move_cost):
        x = move_cost
        y = 0
        max_gradient_pos = -1
        max_gradient = -100

        for i in range(0, len(yield_array)):
            y += yield_array[i]
            x += dig_cost
            m = y / x
            if m > max_gradient:
                max_gradient = m
                max_gradient_pos = i

        return max_gradient_pos