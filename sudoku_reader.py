import hulpfunctions as hf
import math


def find_dimensions(sudoku_game:str)->int:
    #find the number of squares in the sudoku and return the square root
    return int(math.sqrt(len(sudoku_game)))

def make_clauses(game_representation:str, dimensions:int)->list:

    #initiate result
    result = []

    #iterate the sudoku and adjust representation accordingly
    for n, x in enumerate(game_representation):
        if x == '.':
            pass
        else:
            # find row index (first index = 1)
            r = int(n/dimensions) + 1
            # find collum index (first index = 1)
            c = n - ((r-1) * dimensions) + 1
            # find which value in that position should become True
            v = int(x)
            result.append(f'{r}{c}{v}')
    return result


def puzzle_to_dimac(sudoku_puzzle, comments:str='No comments') -> dict:

    #strip string of unnecessary
    sudoku_puzzle = sudoku_puzzle.strip('\n')

    #read dimensions (4x4, 9x9, etc.)
    dimensions = find_dimensions(sudoku_puzzle)

    #translate puzzle to clauses
    clauses = make_clauses(sudoku_puzzle, dimensions=dimensions)
    
    #first line includes comments
    first_line = 'c ' + comments

    #header line describes content: problem, cnf form, num of variables, num of clauses
    header_line = f'p cnf {len(clauses)} {len(clauses)}'

    #transform clause to correct DIMAC format
    dimac_clauses = ' 0\n'.join(clauses)

    #return all elements combined
    return {'dimensions':dimensions, 
            'num_of_clauses':len(clauses), 
            'dimac':f'{first_line}\n{header_line}\n{dimac_clauses} 0'}

def rule_reader(dimensions:int) -> dict:
    #read corresponding rules file
    rules_file_parent = 'Rules/'
    rules_file_name = f'sudoku-rules-{dimensions}x{dimensions}.txt'

    #retrieve ruleset for respected dimensions
    rule_set = hf.read_text_file(file_path=rules_file_parent+rules_file_name)
    
    for n, line in enumerate(rule_set):
        #remove possible whitespaces
        line = line.strip()

        #the comment line
        if line.startswith('c'):
            pass
        #the header line
        elif line.startswith('p'):
            #remove '\n' and split in spaces to identify the individual elements
            header = line.strip('\n').split()
            #save variables from the header
            num_of_clauses = int(header[-1])
            num_of_variables = int(header[-2])
            
            break
        
    #return as dict: the number of variables, number of clauses and the clauses
    return {'num_of_variables': num_of_variables,
            'num_of_clauses': num_of_clauses,
            'rule_clauses': ''.join(rule_set[n+1:])}

def puzzle_and_rules_to_dimac(sudoku_puzzle):
    puzzle_dict = puzzle_to_dimac(sudoku_puzzle=sudoku_puzzle)
    rules_dict = rule_reader(dimensions=puzzle_dict['dimensions'])

    #calculate new number of clauses
    new_num_of_clauses = puzzle_dict['num_of_clauses'] + rules_dict['num_of_clauses']

    #create new header line
    new_header_line = f'p cnf {rules_dict["num_of_variables"]} {new_num_of_clauses}'

    #seperate lines from dimac form
    puzzle_lines = puzzle_dict["dimac"].split("\n")

    #combine the clauses from the puzzle as string
    puzzle_clauses = "\n".join(puzzle_lines[2:])

    #return as string: the comment line, header line, clauses from puzzle and clauses from rules
    return f'{puzzle_lines[0]}\n\
{new_header_line}\n\
{puzzle_clauses}\n\
{rules_dict["rule_clauses"]}'


def create_input(filename:str, num_of_games:int=1, print:bool=False):

    #debug/print variables
    length_of_print_per_game = 200

    input_file_parent = 'Datasets/'
    input_file_name = filename

    #read file
    input = hf.read_text_file(file_path=input_file_parent+input_file_name)
    
    #return the represention
    return [puzzle_and_rules_to_dimac(game) for game in input[:num_of_games]]

if __name__ == '__main__':

    # works for sudokus 9x9 and smaller

    #debug/print variables
    num_of_games = 1
    length_of_print_per_game = 200

    input_file_parent = 'Datasets/'
    input_file_name = 'top91.sdk.txt'

    #read file
    input = hf.read_text_file(file_path=input_file_parent+input_file_name)
    
    #return the represention
    for game in input[:num_of_games]:
        # break
        print(puzzle_and_rules_to_dimac(game)[:length_of_print_per_game])