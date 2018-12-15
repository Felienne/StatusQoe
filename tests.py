import unittest
import board

class MyTestCase(unittest.TestCase):

  def test_statenumber_equal(self):
    b1 = board.Board(map(int, "012212021"))
    b2 = board.Board(map(int, "021121012"))

    self.assertEqual(b1.state_number(1), b2.state_number(2))

  def test_winner_2(self):
    b1 = board.Board(map(int, "012212022"))

    self.assertEqual(2, b1.winner())

  def test_winner_0(self):
    b1 = board.Board(map(int, "010002002"))

    self.assertEqual(0, b1.winner())

  def test_play_then_win(self):
    b1 = board.Board()
    b1 = b1.play(1, 0)
    b1 = b1.play(1, 1)
    b1 = b1.play(1, 2)
    self.assertEqual(1, b1.winner())




if __name__ == '__main__':
  unittest.main()
