from minefactory import *
from yieldgenerator import *
from cuegenerator import *

from logger import event_logger

# class to represent an instance of a game
class Game:

    def __init__(self, time_remaining, no_mines, max_yield, depth, scan_accuracy, dig_cost, move_cost,
                 yield_generator, cue_generator, name, player):
        self.mine_list = []
        self.mine_position = 0
        self.player_gold = 0
        self.scan_accuracy = scan_accuracy
        self.max_yield = max_yield
        self.time_remaining = time_remaining
        self.no_mines = no_mines
        self.depth = depth
        self.dig_cost = dig_cost
        self.move_cost = move_cost
        self.current_mine = None
        self.current_block = None
        self.yield_generator = yield_generator
        self.cue_generator = cue_generator
        self.name = name
        self.gold_in_mine = 0
        self.player = player
        print self.player

        mine_factory = MineFactory(self.yield_generator, self.cue_generator)
        for i in range(self.no_mines):
            new_mine = mine_factory.create_mine(self.depth, self.max_yield, self.scan_accuracy, self.dig_cost,
                                                self.move_cost)
            self.mine_list.append(new_mine)	

    # function to check if the player has chosen to perform a move that is valid
    @staticmethod
    def check_move(player_move):
        if player_move in ['D', 'd', 'M', 'm']:
            return 1
        return 0

    # function to create a mine factory and construct a game consisting of several mines
    # will be used during GUI implementation to begin prompting the user
    def start(self):
        self.current_mine = self.mine_list[self.mine_position]
        self.current_block = self.current_mine.get_current_block()

    def get_current_blocks(self):
        return self.mine_list[self.mine_position].block_list

    # function to return the current state of the game
    def get_state(self):
        state_dict = {"mine_pos": self.mine_position + 1,
                      "block_pos": self.current_mine.get_block_position() + 1,
                      "mine_optimal_stop": self.current_mine.get_optimal() + 1,
                      "no_mines": self.no_mines,
                      "depth": self.depth,
                      "player_gold": self.player_gold,
                      "time_remaining": self.time_remaining,
                      "gold_cue": self.current_block.get_cue()}
        return state_dict

    # function to check for no time remaining and the game being over
    def check_end(self):
        if (self.time_remaining == 0 or
            (self.current_mine.mine_exhausted() and
                ((self.time_remaining <= self.move_cost) or
                    self.mine_list_exhausted()))):
            return 1
        return 0

    def check_mine(self):
        if self.self.current_mine.mine_exhausted():
            return 1
        return 0

    # function to check the player has enough time to move to another mine
    def check_time(self):
        if self.move_cost < self.time_remaining:
            return 1
        return 0

    # function to check if the player has reached the last mine in the mine list
    def mine_list_exhausted(self):
        if self.mine_position == self.no_mines - 1:
            return 1
        return 0

    # function that digs a single block and adds the gold found to the players total
    def player_dig(self):
        gold_collected = self.current_block.get_yield()
        self.player_gold += gold_collected
        self.time_remaining -= self.dig_cost
        self.current_mine.inc_block_pos()
        if not self.current_mine.mine_exhausted():
            self.current_block = self.current_mine.get_current_block()
        self.gold_in_mine += gold_collected
        return gold_collected

    # function that moves the player to the next available mine and puts them back above ground (block 0)
    def player_move(self):
        event_logger.info('USER ' + str(self.player) + ' MINE ' + str(self.name) + ' GOLD ' + str(self.gold_in_mine) + ' OPTIMAL ' \
        + str(self.mine_list[self.mine_position].optimal) + ' MOVE ' + str(self.mine_list[self.mine_position].block_position))
        self.mine_position += 1
        self.current_mine = self.mine_list[self.mine_position]
        self.current_block = self.current_mine.get_current_block()
        self.time_remaining -= self.move_cost

    def get_max_yield(self):
        return self.max_yield

    def get_optimal_game_yield(self):
        optimal_sum = 0
        time = self.time_remaining;

        i = 0
        while time > 0:
            current_mine = self.mine_list[i];
            if (current_mine.optimal * self.dig_cost) < time:
                optimal_sum += self.mine_list[i].optimal_yield
                time -= current_mine.optimal * self.dig_cost
                i += 1
                time -= self.move_cost
            else:
                for j in range(0, self.depth):
                    optimal_sum += current_mine.block_list[j].get_yield()
                    time -= self.dig_cost
                    if time <= 0:
                        break
        return optimal_sum