from minefactory import *
from yieldgenerator import *
from cuegenerator import *

# class to represent an instance of a game


class Game:

    def __init__(self, time_remaining, no_mines, depth):
        self.mine_list = []
        self.mine_position = 0
        self.player_gold = 0
        self.time_remaining = time_remaining
        self.no_mines = no_mines
        self.depth = depth
        self.current_mine = None
        self.current_block = None

    # function to create a mine factory and construct a game consisting of several mines
    def start_game(self, max_yield, yield_generator, cue_generator, scan_accuracy):
        mine_factory = MineFactory(yield_generator, cue_generator)
        for i in range(self.no_mines):
            new_mine = mine_factory.create_mine(self.depth, max_yield, scan_accuracy)
            self.mine_list.append(new_mine)
        self.current_mine = self.mine_list[self.mine_position]
        self.current_block = self.current_mine.get_current_block()

    # function to return the current state of the game
    def get_state(self):
        state_dict = {"mine_pos": self.mine_position + 1,
                      "block_pos": self.current_mine.get_block_position(),
                      "player_gold": self.player_gold,
                      "time_remaining": self.time_remaining,
                      "gold_cue": self.current_block.get_cue()}
        return state_dict

    # function to return the players current gold total
    def get_player_gold(self):
        return self.player_gold

    # function to check for no time remaining and the game being over
    def check_end(self):
        if self.time_remaining != 0:
            return 0

    # function to check the player has enough time to perform the action they have selected
    def check_enough_time(self, action_cost):
        if action_cost < self.time_remaining:
            return 1
        else:
            return 0

    # function to check if the player has reached the last mine in the mine list
    def mine_list_exhausted(self):
        if self.mine_position == self.no_mines - 1:
            return 1
        else:
            return 0

    # function that digs a single block and adds the gold found to the players total
    def player_dig(self, dig_cost):
        gold_collected = self.current_block.get_yield()
        self.current_block = self.current_mine.get_next_block()
        self.player_gold += gold_collected
        self.time_remaining -= dig_cost
        return gold_collected

    # function that moves the player to the next available mine and puts them back above ground (block 0)
    def player_move(self, move_cost):
            self.mine_position += 1
            self.current_mine = self.mine_list[self.mine_position]
            self.current_block = self.current_mine.get_current_block()
            self.time_remaining -= move_cost
