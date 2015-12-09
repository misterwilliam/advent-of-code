import itertools
import unittest

data = """Faerun to Norrath = 129
Faerun to Tristram = 58
Faerun to AlphaCentauri = 13
Faerun to Arbre = 24
Faerun to Snowdin = 60
Faerun to Tambi = 71
Faerun to Straylight = 67
Norrath to Tristram = 142
Norrath to AlphaCentauri = 15
Norrath to Arbre = 135
Norrath to Snowdin = 75
Norrath to Tambi = 82
Norrath to Straylight = 54
Tristram to AlphaCentauri = 118
Tristram to Arbre = 122
Tristram to Snowdin = 103
Tristram to Tambi = 49
Tristram to Straylight = 97
AlphaCentauri to Arbre = 116
AlphaCentauri to Snowdin = 12
AlphaCentauri to Tambi = 18
AlphaCentauri to Straylight = 91
Arbre to Snowdin = 129
Arbre to Tambi = 53
Arbre to Straylight = 40
Snowdin to Tambi = 15
Snowdin to Straylight = 99
Tambi to Straylight = 70"""

def GenPaths(cities):
  for path in _GenPathsRec([], list(cities)):
    yield path

def _GenPathsRec(stack, cities):
    if len(cities) == 0:
        yield stack
    else:
        for i in xrange(len(cities)):
            for path in _GenPathsRec(stack + [cities[i]], cities[:i] + cities[i+1:]):
                yield path

def CalcDistance(start, dest, distancePairs):
    return distancePairs[frozenset((start, dest))]

def CalcPathLength(path, distance_pairs):
    length = 0
    for i in xrange(len(path) - 1):
        length += CalcDistance(path[i], path[i+1], distance_pairs)
    return length

def LoadData(data):
    distance_pairs = {}
    cities = set()
    for line in data.split("\n"):
        start, _, dest, _, distance = line.split()
        cities.add(start)
        cities.add(dest)
        distance_pairs[frozenset([start, dest])] = int(distance)
    return cities, distance_pairs

# ANSWER --------------------------------

cities, distance_pairs = LoadData(data)
longestLength = -1
for path in GenPaths(cities):
    length = CalcPathLength(path, distance_pairs)
    longestLength = max(longestLength, length)
print longestLength

# TESTS ---------------------------------

class GenPathsTests(unittest.TestCase):

  def test_GenPaths(self):
    self.assertEqual(
        [path for path in GenPaths("abcd")],
        [list(permutation) for permutation in itertools.permutations("abcd")])


class CalcPathLengthTests(unittest.TestCase):

  def test_CalcPathLength(self):
    distance_pairs = {
        frozenset(["a", "b"]): 10,
        frozenset(["b", "c"]): 20
    }
    self.assertEqual(CalcPathLength(["a", "b", "c"], distance_pairs), 30)

if __name__ == "__main__":
  unittest.main()