from board import Board
import random
import pickle

class Q_table:

  def __init__(self):
    self.table = [[0.0]*9 for x in range(3**9)]

  def save_to_file(self):
    with open("q_table.p", "wb") as f:
      pickle.dump(self.table, f)

  def read_from_file(self):
    try:
      with open("q_table.p", "rb") as f:
        self.table = pickle.load(f)
    except IOError:
      pass

q = Q_table()
learning_rate = 0.8
discount_rate = 0.95





def choose_random_play(board, player):
  legal_fields = board.get_legal_fields()
  return random.choice(legal_fields)

def q_table_real_play(board, player):
  state_number = board.state_number(player)
  q_values = q.table[state_number]

  legal_fields = board.get_legal_fields()
  legal_moves_according_to_weight = [(m,w) for m,w in enumerate(q_values) if m in legal_fields]

  my_move = pick_max(legal_moves_according_to_weight)
  return my_move


def q_table_play_train(board, player):
  state_number = board.state_number(player)
  q_values = q.table[state_number]

  legal_fields = board.get_legal_fields()
  legal_moves_according_to_weight = [(m,w) for m,w in enumerate(q_values) if m in legal_fields]

  #we need a bit of random noise added to choices, so that moves with 0 weight still
  #have a shot to be explored (otherwise you get stuck in 1 path)
  # 1 is chosen after careful consideration ;-)

  chosen_field = pull_from_distribution(legal_moves_according_to_weight, noise=10)

  #---- now we update the Q-table
  # Because we are a 2-player game, we must first pick the best move for
  # our opponent, and only then can we calculate our own future best move
  # (from that next state)
  new_board = board.play(player, chosen_field)


  opponent = player % 2 + 1
  winner = new_board.winner()

  immediate_reward = 0.5
  if winner == player:
    immediate_reward = 100.0
  elif winner == opponent:
    immediate_reward = -100.0
  elif winner == 3:
    immediate_reward = 50.0


  # Future reward
  next_state_number = new_board.state_number(opponent)
  opponent_best_move = pick_max(enumerate(q.table[next_state_number]))

  new_new_board = new_board.play(opponent, opponent_best_move)
  our_next_move_max_q = max(q.table[new_new_board.state_number(player)])


  # de update functie is:
  # Q[s,a] = Q[s,a] + lr*(r + y*np.max(Q[s1,:]) - Q[s,a])

  q.table[state_number][chosen_field] += learning_rate * (immediate_reward + discount_rate * our_next_move_max_q - q.table[state_number][chosen_field])

  # Because we have negative rewards, this could have gone below 0. Clip to 0.
  if q.table[state_number][chosen_field] < 0:
    q.table[state_number][chosen_field] = 0

  return chosen_field


def pull_from_distribution(distribution, noise):
  """Pull a value from distribution, given a list of (element, weight) pairs"""

  #total_elements_by_weight = flatmap(distribution, lambda element_and_weight: [element_and_weight[0]] * int(noise + element_and_weight[1] * 100))
  #return random.choice(total_elements_by_weight)

  distribution = list(distribution)  # Reify potential generator

  weight_sum = sum(w for x, w in distribution) + noise * len(distribution)
  rand_pick = random.random() * weight_sum

  sum_so_far = 0
  for x, weight in distribution:
    sum_so_far += weight + noise
    if rand_pick < sum_so_far:
      return x
  return distribution[-1][0]


def pick_max(distribution):
  """Pick the value with the max weight from a list of (element, weight) pairs."""
  distribution = list(distribution)  # Reify potential generator
  max_w = max(w for x, w in distribution)
  opts = [x for x, w in distribution if w == max_w]
  return random.choice(opts)


def flatmap(xs, f):
  ret = []
  for x in xs:
    ret.extend(f(x))
  return ret




def main():

  q.read_from_file()

  max_train_games = 0
  max_stats_games = 1000

  wins = [0,0,0,0] #wins of player 1 as 1sr and 2nd player, then of player 2 (1st, 2nd)
  algorithms = [q_table_play_train, q_table_play_train]

  for i in range(max_train_games):
    if i % 10000 == 0:
      q.save_to_file()
      print(i)

    play_one_game(algorithms)

  printed = False

  algorithms = [choose_random_play, q_table_real_play]
  for i in range(max_stats_games):
    (board,start_player, all_boards) = play_one_game(algorithms)

    if board.winner() != 3:
      #print("and the winner is {0} in {1} moves".format(board.winner(), aantal_zetten))

      wins[(board.winner()-1)*2+(start_player-1)] += 1


    if board.winner() == 1 and not printed:
      the_player = start_player
      for b in all_boards:
        b.print()
        print('Q from perspective of %s: %s' % (the_player, q.table[b.state_number(the_player)]))
        the_player = the_player % 2 + 1
      printed = True

  print(round((max_stats_games-sum(wins))/(max_stats_games+1)*100.0,2), [round(w/(max_stats_games+1)*100.0,2) for w in wins])



  q.save_to_file()

def play_one_game(algorithms):
  board = Board()
  all_boards = [board]
  current_player = random.choice([1, 2])
  start_player = current_player
  while board.winner() == 0:
    board = board.play(current_player, algorithms[current_player - 1](board, current_player))
    current_player = current_player % 2 + 1
    all_boards.append(board)

  return (board, start_player, all_boards)


if __name__ == '__main__':
  main()
