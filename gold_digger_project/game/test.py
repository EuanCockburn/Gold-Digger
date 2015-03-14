from yieldgenerator import *
from cuegenerator import *
import random
from functools import partial


def get_optimal(yield_array, dig_cost, move_cost):
        x = move_cost
        y = 0
        max_m_pos = -1
        max_m = -100

        for i in range(0, len(yield_array)):
            y += yield_array[i]
            x += dig_cost
            m = y / x
            if m > max_m:
                max_m = m
                max_m_pos = i

        return max_m_pos

depth = 10
max_yield = 75
slope = 6
dig = 5
move = 20

rand = RandomYield(depth, max_yield).generate_array()
print "Random", rand, get_optimal(rand, dig, move)
const = ConstantYield(depth, max_yield).generate_array()
print "Constant", const , get_optimal(const, dig, move)
print "Linear", LinearYield(depth, max_yield, 20).generate_array()
quad = QuadraticYield(depth, max_yield, 2, 5).generate_array()
print "Quadratic", quad, get_optimal(quad, dig, move)
print "Exponential", ExponentialYield(depth, max_yield).generate_array(2.5, 4)
print "Cubic", CubicYield(depth, max_yield).generate_array(0.5)

span = [-15, 5]
k = random.randint(30, 50) + random.choice(span)
list = [15, 20, 25, 35, 45, 50, 55]
print "Yukon", RandMaxYield(depth, 55, 1, 0, list).generate_array()

span = [10, 12, 15, 20]
print "Brazil", RandMaxYield(depth, 20, -1.5, 5, span).generate_array()

list = [80, 83, 85, 87, 90, 92, 95]
scot = RandMaxYield(depth, 95, 0.7, random.randint(-8, -2), list).generate_array()
print "Scotland", scot, get_optimal(scot, dig, move)

span = [0.2, 0.1, 0.3, 6, 8]
list = [47, 48, 49, 50, 51, 52, 53]
southa = RandMaxYield(depth, 53, random.choice(span), 0, list).generate_array()
print "South Africa", southa, get_optimal(southa, dig, move)

span = [10, -20]
list = [40, 50, 60, 70, 80, 90, 100, 110]
victoria = RandMaxYield(depth, 110, 1, 3, list).generate_array()
print "Victoria", victoria, get_optimal(victoria, dig, move)

cali = RandUniformAdjustYield(depth, 25, 1, -2, 2).generate_array()
print "\nCalifornia", cali
print AccurateCue(25, 0.2).generate_array(cali)

