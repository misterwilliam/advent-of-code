import collections
import re
import unittest

class Transformation(object):

  def __init__(self, input, output):
    self.input = input
    self.output = output

  def gen_transformations(self, string):
    for match in find_matches(string, self.input):
      yield replace(string, match, self.output)

  def reverse(self, string):
    for match in find_matches(string, self.output):
      yield replace(string, match, self.input)

  def __str__(self):
    return "%s => %s" % (self.input, self.output)

  @staticmethod
  def load_from_string(string):
    tokens = string.split()
    return Transformation(tokens[0], tokens[2])

def find_matches(string, pattern):
  for i in xrange(len(string) - len(pattern) + 1):
    if string[i:i + len(pattern)] == pattern:
      yield (i, i + len(pattern))

def replace(string, range, replacement):
  return string[:range[0]] + replacement + string[range[1]:]

def bfs_search(seed, target, transformations):
  todo = collections.deque()
  seen = set()
  todo.append((seed, 0))
  seen.add(seed)
  prev_num_steps = 0
  while len(todo) > 0:
    current, num_steps = todo.popleft()
    for transformation in transformations:
      for output in transformation.gen_transformations(current):
        if len(output) > len(target):
          continue
        if output == target:
          return num_steps + 1
        if output not in seen:
          seen.add(output)
          todo.append((output, num_steps + 1))
    if num_steps != prev_num_steps:
      print "Progress", num_steps, len(todo)
      prev_num_steps = num_steps


# ANSWER ------------------
data = """Al => ThF
Al => ThRnFAr
B => BCa
B => TiB
B => TiRnFAr
Ca => CaCa
Ca => PB
Ca => PRnFAr
Ca => SiRnFYFAr
Ca => SiRnMgAr
Ca => SiTh
F => CaF
F => PMg
F => SiAl
H => CRnAlAr
H => CRnFYFYFAr
H => CRnFYMgAr
H => CRnMgYFAr
H => HCa
H => NRnFYFAr
H => NRnMgAr
H => NTh
H => OB
H => ORnFAr
Mg => BF
Mg => TiMg
N => CRnFAr
N => HSi
O => CRnFYFAr
O => CRnMgAr
O => HP
O => NRnFAr
O => OTi
P => CaP
P => PTi
P => SiRnFAr
Si => CaSi
Th => ThCa
Ti => BP
Ti => TiTi
e => HF
e => NAl
e => OMg"""
target = "CRnCaCaCaSiRnBPTiMgArSiRnSiRnMgArSiRnCaFArTiTiBSiThFYCaFArCaCaSiThCaPBSiThSiThCaCaPTiRnPBSiThRnFArArCaCaSiThCaSiThSiRnMgArCaPTiBPRnFArSiThCaSiRnFArBCaSiRnCaPRnFArPMgYCaFArCaPTiTiTiBPBSiThCaPTiBPBSiRnFArBPBSiRnCaFArBPRnSiRnFArRnSiRnBFArCaFArCaCaCaSiThSiThCaCaPBPTiTiRnFArCaPTiBSiAlArPBCaCaCaCaCaSiRnMgArCaSiThFArThCaSiThCaSiRnCaFYCaSiRnFYFArFArCaSiRnFYFArCaSiRnBPMgArSiThPRnFArCaSiRnFArTiRnSiRnFYFArCaSiRnBFArCaSiRnTiMgArSiThCaSiThCaFArPRnFArSiRnFArTiTiTiTiBCaCaSiRnCaCaFYFArSiThCaPTiBPTiBCaSiThSiRnMgArCaF"
transformations = []
for line in data.split("\n"):
  transformations.append(Transformation.load_from_string(line))
transformations.sort(key=lambda x: len(x.output), reverse=True)

current = target
num_steps = 0
while current != "e":
  did_step = False
  for transformation in transformations:
    candidates = [candidate for candidate in transformation.reverse(current)]
    if candidates:
      current = candidates[0]
      num_steps += 1
      did_step = True
      break
  print num_steps, current
  if not did_step:
    print num_steps, current
    break
print num_steps
#print bfs_search("e", target, transformations)


# TESTS -------------------

class MyTests(unittest.TestCase):

  def test_replace(self):
    self.assertEqual(replace("abcde", (2, 4), "xx"), "abxxe")

  def test_find_matches(self):
    matches = [match for match in find_matches("asdfas", "as")]
    self.assertEqual([(0, 2), (4, 6)], matches)

  def test_gen_transformations(self):
    t = Transformation("xx", "a")
    outputs = [output for output in t.gen_transformations("xxxx")]
    self.assertEqual(["axx", "xax", "xxa"], outputs)

  def test_load_from_string(self):
    transformation = Transformation.load_from_string("Ti => TiTi")
    self.assertEqual("Ti", transformation.input)
    self.assertEqual("TiTi", transformation.output)

  def test_bfs_search(self):
    transformations = [Transformation("a", "b"), Transformation("b", "c"),
      Transformation("c", "d"), Transformation("a", "x"), Transformation("x", "a")]
    num_steps = bfs_search("a", "d", transformations)
    self.assertEqual(3, num_steps)

  def test_bfs_search_has_shortcut(self):
    transformations = [Transformation("a", "b"), Transformation("b", "c"),
      Transformation("c", "d"), Transformation("b", "d")]
    num_steps = bfs_search("a", "d", transformations)
    self.assertEqual(2, num_steps)

if __name__ == "__main__":
  unittest.main()