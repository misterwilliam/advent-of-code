import string
import unittest

letter_map = {letter: i for i, letter in enumerate(string.ascii_lowercase)}

def increment_password(password):
  # start at end
  i = len(password) - 1
  incremented_password_portion = []
  while True:
    # if got to beginning, add 'a' and return new_password
    if i == -1:
      return 'a' + "".join(incremented_password_portion)

    current_char = password[i]
    if current_char == 'z':
      incremented_password_portion.append('a')
      i -= 1
    else:
      char_index = letter_map[current_char]
      new_password = password[:i] + string.ascii_lowercase[char_index + 1] + \
          "".join(incremented_password_portion)
      return new_password

def has_straight(password):
  for i in xrange(len(password) - 2):
    first_char_index = letter_map[password[i]]
    second_char_index = letter_map[password[i + 1]]
    third_char_index = letter_map[password[i + 2]]
    if first_char_index + 1 == second_char_index and \
          second_char_index + 1 == third_char_index:
      return True
  else:
    return False

forbidden_letters = set(["i", "o", "l"])

def has_forbidden_letters(password, forbidden_letters):
  for char in password:
    if char in forbidden_letters:
      return True
  else:
    return False

def has_nonoverlapping_pairs(password):
  i = 0
  found_first_pair = False
  while i < len(password) - 1:
    if password[i] == password[i+1]:
      if found_first_pair:
        return True
      else:
        i += 1
        found_first_pair = True
    i += 1
  else:
    return False

def get_next_password(password):
  current_password = password
  while True:
    current_password = increment_password(current_password)
    if has_straight(current_password) and \
        not has_forbidden_letters(current_password, forbidden_letters) and \
        has_nonoverlapping_pairs(current_password):
      return current_password

# ANSWER ------------------------

print get_next_password(get_next_password("hxbxwxba"))

# TESTS -------------------------


class MyTests(unittest.TestCase):

  def test_increment_password(self):
    self.assertEqual(increment_password("a"), "b")
    self.assertEqual(increment_password("z"), "aa")
    self.assertEqual(increment_password("bz"), "ca")

  def test_has_straight(self):
    self.assertTrue(has_straight("abc"))
    self.assertTrue(has_straight("xabc"))
    self.assertTrue(has_straight("abcx"))
    self.assertFalse(has_straight("abd"))
    self.assertFalse(has_straight("ab"))

  def test_has_forbidden_letters(self):
    self.assertTrue(has_forbidden_letters("i", set(["i"])))

  def test_has_nonoverlapping_pairs(self):
    self.assertTrue(has_nonoverlapping_pairs("aabb"))
    self.assertFalse(has_nonoverlapping_pairs("aaa"))

  def test_get_next_password(self):
    self.assertEqual(get_next_password("abcdefgh"), "abcdffaa")
    self.assertEqual(get_next_password("ghijklmn"), "ghjaabcc")


if __name__ == "__main__":
  unittest.main()