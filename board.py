# 0 is er ligt niks
# 1 is x
# 2 is 0


class Board:

  def __init__(self, fields = None):
    if fields == None:
      self.board = [0]*9 #0 betekent er ligt niks op het bord
    else:
      self.board = list(fields)

  def get_legal_fields(self):
    ret = []
    for i in range(9):
      if self.board[i] == 0:
        ret.append(i)
    return ret

  def play(self, player, field):
    b = Board(self.board)
    b.board[field] = player
    return b

  def from_perspective_of(self, player):
    if player == 1:
      return self
    else:
      b = Board(self.board)
      for i,field in enumerate(b.board):
        if field != 0:
          b.board[i] = 3-field #dit verandert een 1 in ene 2 en een 2 in een 1 en moet perse zo van Rico

      return b

  def state_number(self, player):
    # het idee van deze functie is het bord (een lijst van 9 getallen 0..2, bijv 012212021)
    # ter vertalen in een decimaal getal alsof dit een terniair getal voorstelt.

    from_perspective = self.from_perspective_of(player)
    ret = 0
    for x in from_perspective.board:
      ret = ret * 3 + x

    return ret

  def at(self, x, y):
    return self.board[y * 3 + x]

  def winner(self):
    for c in COMBOS:
      if self.board[c[0]] == self.board[c[1]] and self.board[c[1]] == self.board[c[2]]:
        return self.board[c[0]]

    return 0



COMBOS = [
  # Horizontal lines
  [0, 1, 2],
  [3, 4, 5],
  [6, 7, 8],
  # Vertical lines
  [0, 3, 6],
  [1, 4, 7],
  [2, 5, 8],
  # Diagonals
  [0, 4, 8],
  [2, 4, 6]
]



