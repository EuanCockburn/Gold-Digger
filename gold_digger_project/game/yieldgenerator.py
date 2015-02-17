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
        gold_yield = randint(0, self.max_yield)
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

    def __init__(self, depth, max_yield, slope):
        YieldGenerator.__init__(self, depth, max_yield)
        #super(LinearYield, self).__init__(depth, max_yield)
        self.slope = slope

    def generate_array(self):
        yield_list = []
        for i in range(self.depth):
            yield_x = LinearYield.linear_graph(self.slope, i, self.max_yield)
            yield_list.append(yield_x)
        return yield_list

    @staticmethod
    def linear_graph(m, x, b):
        y = -(m*x) + b

        if y < 0:
            return 0

        return y


# class to return an array of gold return that decreases quadratically as the player digs further into the mine
class QuadraticYield(YieldGenerator):

    def __init__(self, depth, max_yield, slope, adjust):
        YieldGenerator.__init__(self, depth, max_yield)
        #super(QuadraticYield, self).__init__(depth, max_yield)
        self.slope = slope
        self.adjust = adjust

    def generate_array(self):
        yield_list = []
        for i in range(self.depth):
            yield_x = QuadraticYield.quadratic_graph(self.slope, self.adjust, self.max_yield, i)
            yield_list.append(yield_x)
        return yield_list

    @staticmethod
    def quadratic_graph(a, k, c, x):
        y = -a*((x-k)**2) + c

        if y < 0:
            return 0

        return int(round(y))


class ExponentialYield(YieldGenerator):

    def generate_array(self, slope, adjust):
        yield_list = []
        for i in range(self.depth):
            yield_x = ExponentialYield.exp_graph(slope, adjust, self.max_yield, i)
            yield_list.append(yield_x)
        return yield_list

    @staticmethod
    def exp_graph(a, k, c, x):
        y = -a**(x-k) + c

        if y < 0:
            return 0

        return int(round(y))


class CubicYield(YieldGenerator):

    def generate_array(self, slope):
        yield_list = []
        for i in range(self.depth):
            yield_x = CubicYield.cubic_graph(slope, self.max_yield, i)
            yield_list.append(yield_x)
        return yield_list

    @staticmethod
    def cubic_graph(a,c,x):
        y = -a*(x**3) + c

        if y < 0:
            return 0

        return int(round(y))