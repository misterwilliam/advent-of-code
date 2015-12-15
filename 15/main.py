import unittest

data = """Sprinkles: capacity 5, durability -1, flavor 0, texture 0, calories 5
PeanutButter: capacity -1, durability 3, flavor 0, texture 0, calories 1
Frosting: capacity 0, durability -1, flavor 4, texture 0, calories 6
Sugar: capacity -1, durability 0, flavor 0, texture 2, calories 8"""

class Matrix(object):

  def __init__(self, data):
    self.data = data
    self.height = len(data)
    if len(data) > 0:
      self.width = len(data[0])
    else:
      self.width = 0
    for row in self.data:
      assert(len(row)) == self.width

  def columns(self):
    for i in xrange(self.width):
      column = []
      for j in xrange(self.height):
        column.append(self.data[j][i])
      yield column

def strip_last_char(string):
  return string[:-1]

def load_payoff_matrix(data):
  rows = []
  ingredients = []
  calorie_counts = []
  for line in data.split("\n"):
    tokens = line.split()
    ingredient, capacity, durability, flavor, texture, calories = (
      strip_last_char(tokens[0]),
      int(strip_last_char(tokens[2])),
      int(strip_last_char(tokens[4])),
      int(strip_last_char(tokens[6])),
      int(strip_last_char(tokens[8])),
      int(tokens[10]),
    )
    ingredients.append(ingredient)
    calorie_counts.append(calories)
    rows.append([capacity, durability, flavor, texture])

  return Matrix(rows), ingredients, calorie_counts

def dot(a, b):
  # total = reduce(operator.add, map(operator.mul, a, b))
  total = 0
  for a_i, b_i in zip(a, b):
    total += a_i * b_i
  return total

def calc_cookie_score(recipe, payoff_matrix):
  score = 1
  for column in payoff_matrix.columns():
    score *= max(dot(recipe, column), 0)
  return score

def gen_mixtures(num_dimensions, sum_value):
  if num_dimensions == 1:
    yield [sum_value]
  else:
    for i in xrange(sum_value, -1, -1):
      for sub_mixture in gen_mixtures(num_dimensions - 1, sum_value - i):
        yield [i] + sub_mixture

def max_mixture_search(num_dimensions, sum_value, payoff_matrix, calorie_counts):
  score = 0
  max_mixture = None
  for mixture in gen_mixtures(num_dimensions, sum_value):
    if dot(mixture, calorie_counts) == 500:
      score, max_mixture = max((calc_cookie_score(mixture, payoff_matrix), mixture),
                               (score, max_mixture))
  return score, max_mixture

# ANSWER ----------------------------------
payoff_matrix, ingredients, calorie_counts = load_payoff_matrix(data)
print max_mixture_search(len(ingredients), 100, payoff_matrix, calorie_counts)

# TESTS -----------------------------------
class MatrixTests(unittest.TestCase):

  def test_EmptyMatrix(self):
    m = Matrix([[]])
    self.assertEqual([[]], m.data)

  def test_NonRectangularInput(self):
    with self.assertRaises(AssertionError):
      m = Matrix([[1,2,3], [1,2]])

  def test_Columns(self):
    m = Matrix([[1, 2, 3],
                [4, 5, 6]])
    columns = [column for column in m.columns()]
    self.assertEqual([[1, 4],
                      [2, 5],
                      [3, 6]],
                     columns)


class CalcCookieScoreTests(unittest.TestCase):

  def test_Basic(self):
    recipe = [1, 2, 3]
    payoff_matrix = Matrix([[1, 2],
                            [3, -4],
                            [-2, 6]])
    score = calc_cookie_score(recipe, payoff_matrix)
    # 1 = dot([1, 2, 3], [1, 3, -2])
    # 12 = dot([1, 2, 3], [2, -4, 6])
    self.assertEqual(score, 12)

class GenMixturesTest(unittest.TestCase):

  def test_TwoColumns(self):
    mixtures = [mixture for mixture in gen_mixtures(2, 4)]
    self.assertEqual(mixtures,
                     [[4, 0],
                      [3, 1],
                      [2, 2],
                      [1, 3],
                      [0, 4]])

  def test_ThreeColumns(self):
    mixtures = [mixture for mixture in gen_mixtures(3, 4)]
    self.assertEqual(mixtures,
                     [[4, 0, 0],
                      [3, 1, 0],
                      [3, 0, 1],
                      [2, 2, 0],
                      [2, 1, 1],
                      [2, 0, 2],
                      [1, 3, 0],
                      [1, 2, 1],
                      [1, 1, 2],
                      [1, 0, 3],
                      [0, 4, 0],
                      [0, 3, 1],
                      [0, 2, 2],
                      [0, 1, 3],
                      [0, 0, 4]])

if __name__ == "__main__":
  unittest.main()