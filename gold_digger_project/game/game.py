from minefactory import *
from yieldgenerator import *
from cuegenerator import *

# import cache and pickle functioning
import pickle
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

    #Function to store game in cache
    def store_game_incache(id, game):
        cache.set(id,pickle.dumps(game), 500)

    #Fucntion to retrieve game from cache
    def get_game_incache(id):
        game = pickle.loads(cache.get(id))
        return game
    
    #Functions used for retrieving game
    def retrieve_game(id):
	return get_game_incache(id)
   
    #Fucntion to call game storage in cache
    def store_game(id, game):
	store_game_incache(id, game)

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
        self.gold_in_mine += self.gold_collected
        return gold_collected

    # function that moves the player to the next available mine and puts them back above ground (block 0)
    def player_move(self):
        event_logger.info('USER ' + self.player + ' MINE ' + self.name + ' GOLD ' + self.gold_in_mine + ' OPTIMAL ' + self.mine_list[self.mine_position].optimal)
        self.mine_position += 1
        self.current_mine = self.mine_list[self.mine_position]
        self.current_block = self.current_mine.get_current_block()
        self.time_remaining -= self.move_cost

    def get_max_yield(self):
        return self.max_yield