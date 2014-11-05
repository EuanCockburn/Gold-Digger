from random import randint

# class to generate an array of cues that give the player an indication of how much gold can potentially be mined from
# the next block in the mine


class CueGenerator:

    def __init__(self, max_yield, scan_accuracy):
        self.max_yield = max_yield
        self.scan_accuracy = scan_accuracy

# classto return an array of randomly generated cues between 0 and the maximum yield


class RandomCue(CueGenerator):

    def generate_array(self, yield_list):
        cue_list = []
        for i in range(len(yield_list)):
            cue = randint(0, self.max_yield)
            cue_list.append(cue)
        return cue_list

# class to return an array of cues generated based on the accuracy of the players current scanning equipment


class AccurateCue(CueGenerator):

    def generate_array(self, yield_list):
        cue_array = []
        scan_inaccuracy = 1 - self.scan_accuracy

        for i in range(len(yield_list)):
            gold_yield = yield_list[i]
            cue_inaccuracy = int(gold_yield * scan_inaccuracy)
            cue_inaccuracy = randint(0, cue_inaccuracy)
            effect = randint(0, 1)

            if effect == 0:
                cue_array.append(gold_yield + cue_inaccuracy)
            else:
                cue_array.append(gold_yield - cue_inaccuracy)

        return cue_array

# class to return an array of blank queues i.e. the player is given no indication of the potential gold return


class BlankCue(CueGenerator):

    def generate_array(self, yield_list):
        cue_list = []
        for i in range(len(yield_list)):
            cue = 0
            cue_list.append(cue)
        return cue_list