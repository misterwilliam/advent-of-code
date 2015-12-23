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
  for elf in get_divisors(house_number):
    if house_number / elf <= houses_per_elf:
      num_presents += presents_per_elf * elf
  return num_presents

def calc_num_presents_finite_visits_fixed(house_number):
  num_presents = 0
  divisors = set(reduce(list.__add__,
                    ([i, house_number//i] for i in range(1, int(house_number**0.5) + 1) if house_number % i == 0)))
  #for elf in get_divisors(house_number):
  for elf in divisors:
    if house_number / elf <= 50:
      num_presents += 11 * elf
  return num_presents

@memeoize
def get_divisors(num):
  i = 2
  while i < (num / 2) + 1:
    if num % i == 0:
      divisors = get_divisors(num / i)
      return set([1, i, num / i, num]) | divisors | set([divisor * i for divisor in divisors])
    i += 1
  return set([1, num])

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

def brute_force_search(func, threshold):
  i = 1
  max_value = 1
  while True:
    value = func(i)
    max_value = max(max_value, value)
    if value >= threshold:
      return i
    if i % 10000 == 0:
      print i, max_value
    i += 1

def list_backed_calc_num_presents(max_house_number, threshold):
  houses = [0 for _ in xrange(max_house_number)]
  print "Initialized array"
  for i in xrange(0, max_house_number):
    j = i
    if i % 1000:
      print i
    while j < len(houses):
      houses[j] += i * 10
      j += i
  for i, house in enumerate(houses):
    if house > threshold:
      return i



# ANSWER ---------------------------
# print brute_force_search(lambda house_number: calc_num_presents_finite_visits(house_number,
#    50, 11), 29000000)

#print brute_force_search(get_presents, 29000000)
#print brute_force_search(calc_num_presents_finite_visits_fixed, 29000000)

# i = 1
# while True:
#     v = get_presents(i)
#     if v > 29000000:
#         print "House", i, "got", v, "presents."
#         break
#     if i % 1000 == 0:
#       print i
#     i += 1
# print calc_num_presents(1124352)
# print calc_num_presents(1124351)

# BENCHMARK ------------------------
class Timer(object):
  def __enter__(self):
    self.start = time.time()
    return self

  def __exit__(self, *args):
    self.end = time.time()
    self.secs = self.end - self.start
    print

target = 100000000000000000000
with Timer() as t:
  get_divisors(target)
print 'get_divisors elapsed time: %f secs' % t.secs

with Timer() as t:
  calc_num_presents_finite_visits_fixed(100000)
print 'calc_num_presents_finite_visits_fixed elapsed time: %f secs' % t.secs

with Timer() as t:
  brute_force_search(calc_num_presents_finite_visits_fixed, 29000)
print 'brute_force_search(calc_num_presents_finite_visits_fixed elapsed time: %f secs' % t.secs

# with Timer() as t:
#   get_factors(target)
# print 'elapsed time: %f secs' % t.secs

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

  def test_calc_num_presents(self):
    self.assertEqual(10, calc_num_presents_finite_visits(1, 10, 10))
    self.assertEqual(30, calc_num_presents_finite_visits(2, 10, 10))
    self.assertEqual(40, calc_num_presents_finite_visits(3, 10, 10))
    self.assertEqual(70, calc_num_presents_finite_visits(4, 10, 10))
    self.assertEqual(120, calc_num_presents_finite_visits(6, 10, 10))
    self.assertEqual(130, calc_num_presents_finite_visits(9, 10, 10))

if __name__ == "__main__":
  unittest.main()