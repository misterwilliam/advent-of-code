import cProfile
import pstats
import time
import unittest

def memeoize(func):
  cache = {}
  def helper(arg):
    if arg not in cache:
      cache[arg] = func(arg)
    return cache[arg]
  return helper

def calc_num_presents(house_number):
  if house_number == 1:
    return 10
  elif house_number == 2:
    return 30
  divisors = get_divisors(house_number)
  num_presents = sum(divisor * 10 for divisor in divisors)
  num_presents += house_number * 10
  return num_presents

def calc_num_presents_finite_visits(house_number, houses_per_elf, presents_per_elf):
  num_presents = 0
  # I should be able to beat one_line_divisor with get_divisor but I can't figure out how.
  for elf in one_line_divisors(house_number):
    if house_number / elf <= houses_per_elf:
      num_presents += presents_per_elf * elf
  return num_presents

def one_line_divisors(house_number):
  return set(
    reduce(list.__add__,
           ([i, house_number//i]
            for i in range(1, int(house_number**0.5) + 1)
            if house_number % i == 0)))

# @memeoize
# def get_divisors(num):
#   i = 2
#   while i < (num / 2) + 1:
#     if num % i == 0:
#       divisors = get_divisors(num / i)
#       return set([1, i, num / i, num]) | divisors | set([divisor * i for divisor in divisors])
#     i += 1
#   return set([1, num])

def get_divisors(num):
  return set([1, num]) | get_factors(num)

@memeoize
def get_factors(num):
  if num < 1000000:
    return one_line_divisors(num)
  i = 2
  while i < (num / 2) + 1:
    if num % i == 0:
      divisors = get_factors(num / i)
      return set([i, num / i]) | divisors | set([divisor * i for divisor in divisors])
    i += 1
  return set()

def exponential_search(func, threshold):
  known_min = 1
  known_max = None
  while known_max is None:
    guess = known_min * 2
    value = func(guess)
    print guess, value
    if value == threshold:
      return guess
    elif value > threshold:
      known_max = guess
    else:  # guess is too small
      known_min = guess
  while True:
    guess = (known_min + known_max) / 2
    value = func(guess)
    print known_min, known_max, guess, value
    if value == threshold:
      return guess
    elif value > threshold:
      known_max = guess
    else:  # guess is too small
      known_min = guess
    if known_max - known_min == 1:
      return known_max

def brute_force_search(func, threshold, verbose=True):
  i = 1
  max_value = 1
  while True:
    value = func(i)
    max_value = max(max_value, value)
    if value >= threshold:
      return i
    if verbose:
      if i % 10000 == 0:
        print i, max_value
    i += 1

# ANSWER ---------------------------
# print brute_force_search(lambda house_number: calc_num_presents_finite_visits(house_number,
#    50, 11), 29000000)

#print brute_force_search(get_presents, 29000000)
#print brute_force_search(calc_num_presents_finite_visits_fixed, 29000000)

# BENCHMARK ------------------------
class Timer(object):
  def __enter__(self):
    self.start = time.time()
    return self

  def __exit__(self, *args):
    self.end = time.time()
    self.secs = self.end - self.start
    print

target = 200000000
with Timer() as t:
  get_divisors(target)
print 'get_divisors elapsed time: %f secs' % t.secs

with Timer() as t:
  one_line_divisors(target)
print 'one_line_divisors elapsed time: %f secs' % t.secs

with Timer() as t:
  calc_num_presents_finite_visits(100000, 50, 11)
print 'calc_num_presents_finite_visits_fixed elapsed time: %f secs' % t.secs

target = 500000
# pr = cProfile.Profile()
# pr.enable()
with Timer() as t:
  brute_force_search(lambda house_number: calc_num_presents_finite_visits(house_number,
        50, 11), target, verbose=False)
print 'brute_force_search(calc_num_presents_finite_visits_fixed elapsed time: %f secs' % t.secs

# sortby = 'tottime'
# ps = pstats.Stats(pr).sort_stats(sortby)
# ps.print_stats()

# TESTS ----------------------------

class MyTests(unittest.TestCase):

  def test_calc_num_presents(self):
    self.assertEqual(10, calc_num_presents(1))
    self.assertEqual(30, calc_num_presents(2))
    self.assertEqual(40, calc_num_presents(3))
    self.assertEqual(70, calc_num_presents(4))
    self.assertEqual(120, calc_num_presents(6))
    self.assertEqual(130, calc_num_presents(9))

  def test_get_divisors(self):
    self.assertEqual(set([1, 2, 3, 4, 6, 12]), get_divisors(12))
    self.assertEqual(set([1, 2]), get_divisors(2))

  def test_get_factors(self):
    self.assertEqual(set([2, 3, 4, 6]), get_factors(12))
    self.assertEqual(set([]), get_factors(2))

  def test_calc_num_presents(self):
    self.assertEqual(10, calc_num_presents_finite_visits(1, 10, 10))
    self.assertEqual(30, calc_num_presents_finite_visits(2, 10, 10))
    self.assertEqual(40, calc_num_presents_finite_visits(3, 10, 10))
    self.assertEqual(70, calc_num_presents_finite_visits(4, 10, 10))
    self.assertEqual(120, calc_num_presents_finite_visits(6, 10, 10))
    self.assertEqual(130, calc_num_presents_finite_visits(9, 10, 10))

if __name__ == "__main__":
  unittest.main()