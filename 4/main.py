import md5
import unittest


def GetDigest(string):
    m = md5.new()
    m.update(string)
    return m.hexdigest()

def DoesStartWithZeros(string, numZeros):
    return string[:numZeros] == "".join("0" for i in xrange(numZeros))

def Mine(string):
    i = 1
    while True:
        digest = GetDigest(string + str(i))
        if DoesStartWithZeros(digest, 5):
            break
        i += 1

    return i

def Mine2(string):
    i = 1
    while True:
        digest = GetDigest(string + str(i))
        if DoesStartWithZeros(digest, 6):
            break
        i += 1

    return i

print Mine2("bgvyzdsv")

class MyTests(unittest.TestCase):

  def test_GetDigest(self):
    self.assertEqual(GetDigest("abcdef609043"), "000001dbbfa3a5c83a2d506429c7b00e")

  def test_DoesStartWithFiveZeros(self):
    self.assertFalse(DoesStartWithZeros("0000x", 5))
    self.assertTrue(DoesStartWithZeros("00000x", 5))

  def test_Mine(self):
    self.assertEqual(Mine("abcdef"), 609043)
    self.assertEqual(Mine("pqrstuv"), 1048970)

if __name__ == "__main__":
  unittest.main()