import collections
import unittest


def gen_valid_combinations(liters, container_sizes):
  first_container_capacity = container_sizes[0]
  if len(container_sizes) == 1:
    if liters == first_container_capacity:
      yield [1]
    elif liters == 0:
      yield [0]
  elif liters == 0:
    yield [0 for _ in xrange(len(container_sizes))]
  else:
    if liters >= first_container_capacity:
      for combination in gen_valid_combinations(liters - first_container_capacity,
                                                container_sizes[1:]):
        yield [1] + combination
    for combination in gen_valid_combinations(liters, container_sizes[1:]):
      yield [0] + combination


# ANSWERS ---------------------------

container_sizes = [
  43,
  3,
  4,
  10,
  21,
  44,
  4,
  6,
  47,
  41,
  34,
  17,
  17,
  44,
  36,
  31,
  46,
  9,
  27,
  38
]

combinations = [combination
  for combination in gen_valid_combinations(150, container_sizes)
]
combinations_by_size = collections.defaultdict(lambda:list())
for combination in combinations:
  combinations_by_size[sum(combination)].append(combination)
for size, combinations in combinations_by_size.iteritems():
  print size, len(combinations)


# TESTS -----------------------------

class MyTests(unittest.TestCase):

  def test_one_container_impossible(self):
    container_sizes = [10]
    combinations = [combination
      for combination in gen_valid_combinations(11, container_sizes)]
    self.assertEqual(combinations, [])

  def test_one_container_possible(self):
    container_sizes = [10]
    combinations = [combination
      for combination in gen_valid_combinations(10, container_sizes)]
    self.assertEqual(combinations, [[1]])

  def test_two_container_possible(self):
    container_sizes = [10, 5]
    combinations = [combination
      for combination in gen_valid_combinations(15, container_sizes)]
    self.assertEqual(combinations, [[1, 1]])

  def test_examples(self):
    container_sizes = [20, 15, 10, 5, 5]
    combinations = [combination
      for combination in gen_valid_combinations(25, container_sizes)]
    self.assertEqual(combinations, [
      [1, 0, 0, 1, 0],
      [1, 0, 0, 0, 1],
      [0, 1, 1, 0, 0],
      [0, 1, 0, 1, 1]])


if __name__ == "__main__":
  unittest.main()