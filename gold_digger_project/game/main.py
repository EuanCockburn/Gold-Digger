from game import *
from yieldgenerator import *
from cuegenerator import *
from time import sleep


time_remaining = 100                                    # the player starts with 300 units of time
no_mines = 20                                           # the game will consist of ten individual mines
depth = 10                                              # each mine will be 10 blocks deep
max_yield = 100                                         # the player has the chance to mine a maximum of 100 gold
scan_accuracy = 0.6                                     # the player's equipment has a predetermined accuracy
dig_cost = 10                                           # the amount of time it takes to dig
move_cost = 15                                          # the amount of time it takes to move to another mine
span = [40, 50, 60, 70, 80, 90, 100, 110]
yield_array = RandMaxYield(depth, 110, 1, 3, span)
cue_generator = AccurateCue(max_yield, scan_accuracy)

game = Game(time_remaining, no_mines, max_yield, depth, scan_accuracy, dig_cost, move_cost,
            yield_array, cue_generator, "test", "test")

game.start()

print "Yield", game.get_optimal_game_yield()
print "\nWelcome to Gold Digger! Try to collect as much gold as you can within the time limit!\n"

while not game.check_end():

    
    game_state = game.get_state()

    print "You are currently located at mine {} of {}, block {} of {}. You are carrying {} gold and have {} " \
          "units of time remaining. Your scanning equipment suggests that there are {} gold pieces to " \
          "be uncovered here.\n".format(game_state.get("mine_pos"), game_state.get("no_mines"),
                                        game_state.get("block_pos"), game_state.get("depth"),
                                        game_state.get("player_gold"), game_state.get("time_remaining"),
                                        game_state.get("gold_cue"))

    print "Do you choose to DIG further into the mine (press D on your keyboard, cost: 20 units)" \
          " or MOVE to a new location in search of another mine (press M on your keyboard, cost: 40 units)?\n"

    player_choice = raw_input("-->")

    while Game.check_move(player_choice) == 0:
        print "\nInvalid choice, please choose to DIG (D) or MOVE (M).\n"
        player_choice = raw_input("-->")

    if player_choice in ['d', 'D']:
        print "\nDigging...\n"
        print "You uncover", game.player_dig(), "gold pieces!\n"
	

        if game.current_mine.mine_exhausted() and not game.check_end():
            print "You have exhausted this mine of its resources and must move on.\n"
            print "You go off in search of your fortune elsewhere...\n"
            print "You stopped digging at block {}, but you should have stopped at block {}. \n"\
                .format(game_state.get("block_pos"), game_state.get("mine_optimal_stop"))

            game.player_move()
        else:
            continue
    else:
        if game.mine_list_exhausted():
            print "\nYou have already explored all of the mines in this area, keep digging!\n"
        elif game.check_time():
            print "\nYou go off in search of your fortune elsewhere...\n"
            print "You stopped digging at block {}, but you should have stopped at block {}. \n"\
                .format(game_state.get("block_pos"), game_state.get("mine_optimal_stop"))
            game.player_move()
        else:
            print "\nThere's not enough time left in the day to go in search of a new mine!\n"

game_state = game.get_state()
print "You stopped digging at block {}, but you should have stopped at block {}. \n"\
    .format(game_state.get("block_pos"), game_state.get("mine_optimal_stop"))

print "Time up! You managed to mine a grand total of ", game_state.get("player_gold"), " gold pieces!\n\nGame Over!"
