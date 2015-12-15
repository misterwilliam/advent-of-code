import itertools
import math
import unittest

data = """Alice would gain 54 happiness units by sitting next to Bob.
Alice would lose 81 happiness units by sitting next to Carol.
Alice would lose 42 happiness units by sitting next to David.
Alice would gain 89 happiness units by sitting next to Eric.
Alice would lose 89 happiness units by sitting next to Frank.
Alice would gain 97 happiness units by sitting next to George.
Alice would lose 94 happiness units by sitting next to Mallory.
Bob would gain 3 happiness units by sitting next to Alice.
Bob would lose 70 happiness units by sitting next to Carol.
Bob would lose 31 happiness units by sitting next to David.
Bob would gain 72 happiness units by sitting next to Eric.
Bob would lose 25 happiness units by sitting next to Frank.
Bob would lose 95 happiness units by sitting next to George.
Bob would gain 11 happiness units by sitting next to Mallory.
Carol would lose 83 happiness units by sitting next to Alice.
Carol would gain 8 happiness units by sitting next to Bob.
Carol would gain 35 happiness units by sitting next to David.
Carol would gain 10 happiness units by sitting next to Eric.
Carol would gain 61 happiness units by sitting next to Frank.
Carol would gain 10 happiness units by sitting next to George.
Carol would gain 29 happiness units by sitting next to Mallory.
David would gain 67 happiness units by sitting next to Alice.
David would gain 25 happiness units by sitting next to Bob.
David would gain 48 happiness units by sitting next to Carol.
David would lose 65 happiness units by sitting next to Eric.
David would gain 8 happiness units by sitting next to Frank.
David would gain 84 happiness units by sitting next to George.
David would gain 9 happiness units by sitting next to Mallory.
Eric would lose 51 happiness units by sitting next to Alice.
Eric would lose 39 happiness units by sitting next to Bob.
Eric would gain 84 happiness units by sitting next to Carol.
Eric would lose 98 happiness units by sitting next to David.
Eric would lose 20 happiness units by sitting next to Frank.
Eric would lose 6 happiness units by sitting next to George.
Eric would gain 60 happiness units by sitting next to Mallory.
Frank would gain 51 happiness units by sitting next to Alice.
Frank would gain 79 happiness units by sitting next to Bob.
Frank would gain 88 happiness units by sitting next to Carol.
Frank would gain 33 happiness units by sitting next to David.
Frank would gain 43 happiness units by sitting next to Eric.
Frank would gain 77 happiness units by sitting next to George.
Frank would lose 3 happiness units by sitting next to Mallory.
George would lose 14 happiness units by sitting next to Alice.
George would lose 12 happiness units by sitting next to Bob.
George would lose 52 happiness units by sitting next to Carol.
George would gain 14 happiness units by sitting next to David.
George would lose 62 happiness units by sitting next to Eric.
George would lose 18 happiness units by sitting next to Frank.
George would lose 17 happiness units by sitting next to Mallory.
Mallory would lose 36 happiness units by sitting next to Alice.
Mallory would gain 76 happiness units by sitting next to Bob.
Mallory would lose 34 happiness units by sitting next to Carol.
Mallory would gain 37 happiness units by sitting next to David.
Mallory would gain 40 happiness units by sitting next to Eric.
Mallory would gain 18 happiness units by sitting next to Frank.
Mallory would gain 7 happiness units by sitting next to George."""

def parse_happiness_line(line):
  guest, would, gain_or_lose, num_happiness, happiness, units, by, sitting, next, to, \
     other_guest = line.split()

  if gain_or_lose == "gain":
    num_happiness = int(num_happiness)
  else:
    num_happiness = -int(num_happiness)

  # Remove trailing period
  other_guest = other_guest[:-1]

  return guest, other_guest, num_happiness

def load_happiness_table(data):
  happiness_table = {}
  guests = set()
  for line in data.split("\n"):
    guest, other_guest, num_happiness = parse_happiness_line(line)
    happiness_table[(guest, other_guest)] = num_happiness
    guests.add(guest)
  return happiness_table, guests

def score_seating_plan(seating_plan, happiness_table):
  happiness = 0
  for i, person in enumerate(seating_plan):
    if person == "you":
      continue
    right_neighbor = seating_plan[i + 1] if i < len(seating_plan) - 1 else seating_plan[0]
    left_neighbor = seating_plan[i - 1] if i > 0 else seating_plan[-1]
    if left_neighbor != "you":
      happiness += happiness_table[(person, left_neighbor)]
    if right_neighbor != "you":
      happiness += happiness_table[(person, right_neighbor)]
  return happiness

def gen_seating_plans(guest_list):
  seating_plan = (guest_list[0],)
  for rest_of_seating_plan in itertools.permutations(guest_list[1:]):
    yield seating_plan + rest_of_seating_plan

# ANSWER ------------------------

happiness_table, guests = load_happiness_table(data)
max_score = 0
guests.add("you")
for seating_plan in gen_seating_plans(list(guests)):
  max_score = max(max_score, score_seating_plan(seating_plan, happiness_table))
print max_score

# TESTS -------------------------

class MyTests(unittest.TestCase):

  def test_score_seating_plan(self):
    happiness_table = {
      ("a", "b"): 3,
      ("a", "c"): -2,
      ("b", "a"): 1,
      ("b", "c"): 1,
      ("c", "a"): 3,
      ("c", "b"): -3,
    }
    self.assertEqual(score_seating_plan(["a", "b", "c"], happiness_table),
                     3)

  def test_gen_seating_plans_correct_length(self):
    seating_plans = [seating_plan for seating_plan in gen_seating_plans(range(10))]
    self.assertEqual(len(seating_plans), math.factorial(10 - 1))

  def test_gen_seating_plans(self):
    seating_plans = [seating_plan for seating_plan in gen_seating_plans("abcd")]
    self.assertEqual(seating_plans, [
        ("a", "b", "c", "d"),
        ("a", "b", "d", "c"),
        ("a", "c", "b", "d"),
        ("a", "c", "d", "b"),
        ("a", "d", "b", "c"),
        ("a", "d", "c", "b"),
      ])


if __name__ == "__main__":
  unittest.main()