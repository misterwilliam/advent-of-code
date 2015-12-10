import unittest


def look_and_say(seq):
  current_run = []
  ret_val = []
  for digit in seq:
    if len(current_run) == 0 or current_run[-1] == digit:
      current_run.append(digit)
    else:  # digit is not part of current run
      ret_val += [len(current_run), current_run[-1]]
      current_run = [digit]
  # Process what remains in current_run
  if len(current_run) > 0:
    ret_val += [len(current_run), current_run[-1]]
  return ret_val


def repeat_look_and_say(seq, num_times):
    ret_val = seq
    for _ in xrange(num_times):
        ret_val = look_and_say(ret_val)
    return ret_val

# ANSWER ---------------

print len(repeat_look_and_say([1, 1, 1, 3, 2, 2, 2, 1, 1, 3], 50))

# TESTS ----------------

class LookAndSayTests(unittest.TestCase):

  def test_examples(self):
    self.assertEqual(look_and_say([1]), [1, 1])
    self.assertEqual(look_and_say([1, 1]), [2, 1])
    self.assertEqual(look_and_say([2, 1]), [1, 2, 1, 1])
    self.assertEqual(look_and_say([1, 2, 1, 1]), [1, 1, 1, 2, 2, 1])
    self.assertEqual(look_and_say([1, 1, 1, 2, 2, 1]), [3, 1, 2, 2, 1, 1])

class RepeatLookAndSayTests(unittest.TestCase):

  def test_examples(self):
    self.assertEqual(repeat_look_and_say([1], 5), [3, 1, 2, 2, 1, 1])


if __name__ == "__main__":
  unittest.main()