import collections
import unittest

data = """Vixen can fly 8 km/s for 8 seconds, but then must rest for 53 seconds.
Blitzen can fly 13 km/s for 4 seconds, but then must rest for 49 seconds.
Rudolph can fly 20 km/s for 7 seconds, but then must rest for 132 seconds.
Cupid can fly 12 km/s for 4 seconds, but then must rest for 43 seconds.
Donner can fly 9 km/s for 5 seconds, but then must rest for 38 seconds.
Dasher can fly 10 km/s for 4 seconds, but then must rest for 37 seconds.
Comet can fly 3 km/s for 37 seconds, but then must rest for 76 seconds.
Prancer can fly 9 km/s for 12 seconds, but then must rest for 97 seconds.
Dancer can fly 37 km/s for 1 seconds, but then must rest for 36 seconds."""

Reindeer = collections.namedtuple('Reindeer', ["name", "km_per_second", "duration_secs",
 "rest_secs"])


def load_data(data):
  reindeer_stats = {}
  for line in data.split("\n"):
    tokens = line.split()
    reindeer_name, km_per_second, duration_secs, rest_secs = (
      tokens[0], tokens[3], tokens[6], tokens[-2])
    reindeer_stats[reindeer_name] = Reindeer(reindeer_name, int(km_per_second),
      int(duration_secs), int(rest_secs))
  return reindeer_stats

def calc_distance(reindeer, secs):
  # Cycle is sprint plus rest cycle
  num_cycles = secs / (reindeer.duration_secs + reindeer.rest_secs)
  distance = num_cycles * reindeer.duration_secs * reindeer.km_per_second
  # Calc distance traveled in incomplete cycle
  extra_time = secs % (reindeer.duration_secs + reindeer.rest_secs)
  if extra_time <= reindeer.duration_secs:
    distance += extra_time * reindeer.km_per_second
  else:
    distance += reindeer.duration_secs * reindeer.km_per_second
  return distance

def get_winner(reindeer_list, current_time):
  distances = []
  for reindeer in reindeer_list:
    distances.append((calc_distance(reindeer, current_time), reindeer))
  return max(distances)[1]

def score_race(reindeer_stats, duration):
  scores = collections.defaultdict(lambda:0)
  for current_time in xrange(1, duration + 1):
    winner = get_winner(reindeer_stats.values(), current_time)
    scores[winner.name] += 1
  return scores


# ANSWER ---------------------
reindeer_stats = load_data(data)
print score_race(reindeer_stats, 2503)

# TESTS ----------------------

class MyTests(unittest.TestCase):

  def test_calc_distance(self):
    comet = Reindeer("Coment", 14, 10, 127)
    self.assertEqual(calc_distance(comet, 3), 42)
    self.assertEqual(calc_distance(comet, 10), 140)
    self.assertEqual(calc_distance(comet, 11), 140)
    self.assertEqual(calc_distance(comet, 137), 140)
    self.assertEqual(calc_distance(comet, 138), 154)
    self.assertEqual(calc_distance(comet, 275), 2 * 14 * 10 + 14)

if __name__ == "__main__":
  unittest.main()