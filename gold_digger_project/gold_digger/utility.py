from game import *
from yieldgenerator import *
from cuegenerator import *
from random import *

time_remaining = 200                                    # the player starts with 300 units of time
no_mines = 10                                           # the game will consist of ten individual mines
depth = 10                                              # each mine will be 10 blocks deep
max_yield = 100                                         # the player has the chance to mine a maximum of 100 gold
scan_accuracy = 0.6                                     # the player's equipment has a predetermined accuracy
dig_cost = 10                                           # the amount of time it takes to dig
move_cost = 60                                          # the amount of time it takes to move to another mine
cue_generator = AccurateCue(max_yield, scan_accuracy)


def california_mine(self, max_gold):
    cali_yield = QuadraticYield(depth, 25).generate_array(1, random.uniform(-2, 2))
    game = Game(time_remaining, no_mines, max_yield, depth, scan_accuracy, dig_cost, move_cost, cali_yield,
                cue_generator)
    return game


def yukon_mine(self, max_gold):
    span = [-15, 5]
    k = random.randint(30, 50) + random.choice(span)
    yuk_yield = QuadraticYield(depth, k).generate_array(1, 0)
    game = Game(time_remaining, no_mines, max_yield, depth, scan_accuracy, dig_cost, move_cost, yuk_yield,
                cue_generator)
    return game


def brazil_mine(self, max_gold):
    span = [10, 12, 15, 20]
    braz_yield = QuadraticYield(depth, random.choice(span)).generate_array(-1.5, 5)
    game = Game(time_remaining, no_mines, max_yield, depth, scan_accuracy, dig_cost, move_cost, braz_yield,
                cue_generator)
    return game


def scotland_mine(self, max_gold):
    scot_yield = QuadraticYield(depth, random.randint(-10, 5) + 90).generate_array(0.7, random.randint(-8, -2))
    game = Game(time_remaining, no_mines, max_yield, depth, scan_accuracy, dig_cost, move_cost, scot_yield,
                cue_generator)
    return game


def south_africa_mine(self, max_gold):
    span = [0.2, 0.1, 0.3, 6, 8]
    southa_yield = QuadraticYield(depth, 50 + random.randint(-3, 3)).generate_array(random.choice(span), 0)
    game = Game(time_remaining, no_mines, max_yield, depth, scan_accuracy, dig_cost, move_cost, southa_yield,
                cue_generator)
    return game


def victoria_mine(self, max_gold):
    span = [10, -20]
    vic_yield = QuadraticYield(depth, random.randint(60, 100) + random.choice(span)).generate_array(1, 3)
    game = Game(time_remaining, no_mines, max_yield, depth, scan_accuracy, dig_cost, move_cost, vic_yield,
                cue_generator)
    return game