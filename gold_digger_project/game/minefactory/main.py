from game import *
from yieldgenerator import *
from cuegenerator import *
from time import sleep

time_remaining = 200                                    # the player starts with 300 units of time
no_mines = 10                                           # the game will consist of ten individual mines
depth = 10                                              # each mine will be 10 blocks deep
max_yield = 100                                         # the player has the chance to mine a maximum of 100 gold
scan_accuracy = 0.6                                     # the player's equipment has a predetermined accuracy
dig_cost = 10                                           # the amount of time it takes to dig
move_cost = 60                                          # the amount of time it takes to move to another mine
yield_generator = RandomYield(depth, max_yield)
cue_generator = AccurateCue(max_yield, scan_accuracy)

game = Game(time_remaining, no_mines, depth)
game.start_game(max_yield, yield_generator, cue_generator, scan_accuracy)

print "\nWelcome to Gold Digger! Try to collect as much gold as you can within the time limit!\n"

while game.check_end() == 0:

    valid_move = False

    game_state = game.get_state()
    print "You are currently located at mine {} of {}, block {} of {}. You are carrying {} gold and have {} " \
          "units of time remaining. Your scanning equipment suggests that there are {} gold pieces to " \
          "be uncovered here.\n".format(game_state.get("mine_pos"), no_mines, game_state.get("block_pos"),
                                        depth, game_state.get("player_gold"), game_state.get("time_remaining"),
                                        game_state.get("gold_cue"))

    print "Do you choose to DIG further into the mine (press D on your keyboard, cost: 20 units)" \
          " or MOVE to a new location in search of another mine (press M on your keyboard, cost: 40 units)?\n"

    while valid_move == 0:
        player_choice = raw_input("-->")

        while player_choice not in ["d", "m", "D", "M"]:
            print "\nInvalid choice, please choose to DIG (D) or MOVE (M).\n"
            player_choice = raw_input("-->")

        if player_choice == "d":
            gold_collected = game.player_dig(dig_cost)
            print "\nDigging...\n"
            sleep(2)
            print "You uncover", gold_collected, "gold pieces!\n"
            valid_move = 1

            if game.current_mine.mine_exhausted() == 1:
                print "You have exhausted this mine of its resources and must move on.\n"
                print "You go off in search of your fortune elsewhere...\n"
                game.player_move(move_cost)
                sleep(3)
        else:
            if game.mine_list_exhausted() == 1:
                print "\nYou have already explored all of the mines in this area, keep digging!\n"
            elif game.check_enough_time(move_cost) == 0:
                print "\nThere's not enough time left in the day to go in search of a new mine!\n"
            else:
                print "\nYou go off in search of your fortune elsewhere...\n"
                game.player_move(move_cost)
                sleep(3)
                valid_move = 1

print "Time up! You managed to mine a grand total of ", game.get_player_gold(), " gold pieces!\n\nGame Over!"





