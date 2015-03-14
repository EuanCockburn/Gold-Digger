from game import *
from yieldgenerator import *
from cuegenerator import *
import unittest

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        self.seq = range(10)
        self.time_remaining = 100
        self.no_mines = 20
        self.depth = 10
        self.max_yield = 100
        self.scan_accuracy = 0.6
        self.dig_cost = 10
        self.move_cost = 15
        self.yield_array = LinearYield(self.depth, self.max_yield, 5)
        self.cue_generator = AccurateCue(self.max_yield, self.scan_accuracy)
        self.game = Game(self.time_remaining, self.no_mines, self.max_yield, self.depth, self.scan_accuracy,
                         self.dig_cost, self.move_cost, self.yield_array, self.cue_generator, "test", "test")
        self.game.start()

    def test_move(self):
        mine_before = self.game.mine_position
        time_before = self.game.time_remaining
        self.game.player_move()
        mine_after = self.game.mine_position
        time_after = self.game.time_remaining
        self.assertEqual(mine_before + 1, mine_after)
        self.assertEqual(time_before, time_after + self.move_cost)

    def test_dig(self):
        gold_before = self.game.player_gold
        time_before = self.game.time_remaining
        self.game.player_dig()
        gold_after = self.game.player_gold
        time_after = self.game.time_remaining
        self.assertEqual(time_before, time_after + self.dig_cost)
        self.assertEqual(gold_before + self.max_yield, gold_after)

