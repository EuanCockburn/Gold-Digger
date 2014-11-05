from yieldgenerator import *
import random

depth = 10
max_yield = 75
slope = 6

print "Random", RandomYield(depth, max_yield).generate_array()
print "Constant", ConstantYield(depth, max_yield).generate_array()
print "Linear", LinearYield(depth, max_yield).generate_array(20)
print "Quadratic", QuadraticYield(depth, max_yield).generate_array(2, 5)
print "Exponential", ExponentialYield(depth, max_yield).generate_array(2.5, 4)
print "Cubic", CubicYield(depth, max_yield).generate_array(0.5)


print "\nCalifornia", QuadraticYield(depth, 25).generate_array(1, random.uniform(-2, 2))

span = [-15, 5]
k = random.randint(30, 50) + random.choice(span)
print "Yukon", QuadraticYield(depth, k).generate_array(1, 0)

span = [10, 12, 15, 20]
print "Brazil", QuadraticYield(depth, random.choice(span)).generate_array(-1.5, 5)

print "Scotland", QuadraticYield(depth, random.randint(-10, 5) + 90).generate_array(0.7, random.randint(-8, -2))

span = [0.2, 0.1, 0.3, 6, 8]
print "South Africa", QuadraticYield(depth, 50 + random.randint(-3, 3)).generate_array(random.choice(span), 0)

span = [10, -20]
print "Victoria", QuadraticYield(depth, random.randint(60, 100) + random.choice(span)).generate_array(1, 3)

