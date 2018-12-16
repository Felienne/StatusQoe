from q_learning import Q_table
import csv


def to_txt_file(q_table):
    with open('q_table.csv', 'w') as csvfile:
      spamwriter = csv.writer(csvfile)
      spamwriter.writerows(q_table.table)


def main():
  q = Q_table()
  q.read_from_file()
  to_txt_file(q)

if __name__ == '__main__':
  main()
