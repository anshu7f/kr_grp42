import sudoku_reader as sr
import dpll
import math


def make_board(solution):
    #find dimensions
    if len(solution) < 3000:
        dimensions = round(len(solution) ** (1/3))
    elif len(solution) < 6000:
        dimensions = 9
    #initiate an empty board (zeros)
    board = {}
    for r in range(dimensions):
        for c in range(dimensions):
            board[f'{r}{c}'] = 0

    if isinstance(solution,  list):

        for x in solution:
            #negated values do not need to be visualised
            if x < 0:
                continue
            # x = str(x)
            # find row index (first row = 1)
            r = str(int(x/100) - 1)
            # r = x[0]
            # find collum index (first index = 1)
            c = str(int((x % 100) /10) - 1)
            # c = x[1]
            # find the correct value
            v = int((x % 10))
            # v = int(x[2])
            # board[r].append([c][v])

            #check if there already is a value
            if board[r + c] > 0:
                assert (f'Dubble value on {r}{c}')
            else:
                board[r + c] = v
    return board


def print_board(board:dict):

    #find dimensions
    dim = round(len(board) ** 0.5)

    #create string for printing to visualise the board
    #initiate the string that will be printed
    pr_str = ''
    for i in range(dim):
        row = ''
        for n in range(dim):
            #create vertical lines for clearity
            if dim == 4: 
                row = row + '| ' if n == 2 else row
            elif dim == 9:
                row = row + '| ' if (n % 3 == 0 and n !=0) else row

            #add value to the row
            row = row + str(board[f'{i}{n}']) + ' '

        #create horizontal lines for clearity
        if dim == 4:
            pr_str = pr_str + ('-'*9) + '\n' if i == 2 else pr_str
        elif dim ==9:
            pr_str = pr_str + ('-'*21) + '\n' if (i % 3 == 0 and i !=0) else pr_str

        #add row to the board
        pr_str = pr_str + row + '\n'

    # print the board
    print(pr_str)

def visualizer(solution):
    board = make_board(solution=solution)
    print_board(board=board)


if __name__ == '__main__':
    cnf = dpll.dpll_algorithm()
    [knowledge_base] = sr.create_input('top91.sdk.txt', cnf_form=True, num_of_games=1)
    # [knowledge_base] = sr.create_input('4x4.txt', cnf_form=True, num_of_games=1)


    if cnf.dpll(knowledge_base):
        print("satisfiable")
        visualizer(cnf.solution)
    else:
        print("unsatisfiable")