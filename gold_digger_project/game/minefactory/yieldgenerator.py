from random import randint

# class to construct an array of gold return for each level or block within a mine


class YieldGenerator:

    def __init__(self, depth, max_yield):
        self.depth = depth
        self.max_yield = max_yield

# class to return an array of gold return that remains constant throughout the mine


class ConstantYield(YieldGenerator):

    def generate_array(self):
        yield_list = []
        gold_yield = randint(self.max_yield)
        for i in range(0, self.depth):
            yield_list.append(gold_yield)
        return yield_list

# class to return an array of gold return that is randomly distributed throughout the mine


class RandomYield(YieldGenerator):

    def generate_array(self):
        yield_list = []
        for i in range(self.depth):
            gold_yield = randint(0, self.max_yield)
            yield_list.append(gold_yield)
        return yield_list

# class to return an array of gold return that decreases linearly as the player digs further into the mine


class LinearYield(YieldGenerator):

    def generate_array(self):
        pass

# class to return an array of gold return that decreases quadratically as the player digs further into the mine


class QuadraticYield(YieldGenerator):

    def generate_array(self):
        pass