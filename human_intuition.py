
import numpy as np
import math
import random

from dpll import dpll_algorithm

import sudoku_reader as sr
import visualise_sudoku as vs

import pandas as pd
from datetime import datetime, timedelta


class Human_intuition(dpll_algorithm):
    def __init__(self, dimensions:int=9) -> None:
        self.dimensions = dimensions
        self.info_matrix = np.zeros([self.dimensions, self.dimensions], dtype=np.int16)
        self.board_rep = np.zeros([self.dimensions, self.dimensions], dtype=np.int16)

        self.solution = []
        self.reset_board = False
        self.count_units = 0
        self.count_lit_choose = 0
        self.step = 0

        self.ninexnine_block_ranges={
                '00': (0,3,0,3),
                '01': (0,3,3,6),
                '02': (0,3,6,9),

                '10': (3,6,0,3),
                '11': (3,6,3,6),
                '12': (3,6,6,9),

                '20': (6,9,0,3),
                '21': (6,9,3,6),
                '22': (6,9,6,9)
                }   
        self.fourxfour_block_ranges={
                '00': (0,2,0,2),
                '01': (0,2,2,4),
                '10': (2,4,0,2),
                '11': (2,4,2,4)
                }
        self.clean_up_time = timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0)
        self.count_backpropagation = 0

    def unit_propagation(self, knowledge_base, litteral):
        start_time_clean_up = datetime.now()
        knowledge_base = [[l for l in clause if l != -1*litteral] for clause in knowledge_base if litteral not in clause]
        end_time_clean_up = datetime.now()
        self.count_units += 1
        #update (information) for choosing litteral
        self.update_boards(litteral)
        self.clean_up_time += (end_time_clean_up - start_time_clean_up)
        return knowledge_base


    def choose_litteral(self, knowledge_base):
        self.count_lit_choose += 1
        row, col = self.find_max_info_position()
        literal = self.find_literal_from_position(r=row, c=col)

        #plus 1 for translation from index to row number
        v_print('suggest: '+ str(literal))

        return literal

    
    def find_block(self, r, c) -> str:
        if self.dimensions == 4:
            #blocks can be {0-2}{0-2}
            block = f'{int(r / 2)}{int(c / 2)}'
        elif self.dimensions == 9:
            #blocks can be {0-3}{0-3}
            block = f'{int(r / 3)}{int(c / 3)}'
        return block

    def block_update(self, r, c):
        #find block identifier
        block = self.find_block(r, c)    

        #find its ranges
        (rx, ry, cx, cy) = self.block_ranges(block)

        #add 1 information point to all corresponding positions
        self.info_matrix[rx:ry, cx:cy] += 1

        return


    def info_update(self, r_i, c_i):
        #add information points to all elements in corresponding row
        self.info_matrix[r_i] = self.info_matrix[r_i] + 1
        #add information points to all elements in corresponding colomn
        self.info_matrix[:, c_i] = self.info_matrix[:, c_i] + 1
        #add information points to all elements inside corresponding block
        self.block_update(r_i, c_i)

        #note that this position is locked (and therefore non interesting for determining next literal)
        self.info_matrix[r_i,c_i] = -10000
        return 

    def find_most_info_pos(self):
        highest = self.info_matrix.argmax()

        row = int(highest / self.dimensions)
        col =  highest % self.dimensions
        return row, col


    def board_representation_update(self, r_i, c_i, v):

        if self.board_rep[r_i,c_i] > 0 and not self.reset_board:
            print('dubble value (index):', r_i,c_i,v)
        self.board_rep[r_i, c_i] = v


    def update_with_literal(self, literal):        
        if literal < 0:
            return

        # find row index (first row = 1)
        row_i = int(literal / 100) - 1
        # find collum index (first index = 1)
        col_i = int((literal % 100) /10) - 1
        # find the correct value
        val = int((literal % 10))

        self.info_update(r_i=row_i, c_i=col_i)
        self.board_representation_update(r_i=row_i, c_i=col_i, v=val)
        return

    def update_boards(self, literal):

        if self.reset_board:
            #done after backpropagation (unkown where it backpropagated, so start over)
            self.info_matrix = np.zeros([self.dimensions, self.dimensions], dtype=np.int16)
            self.board_rep = np.zeros([self.dimensions, self.dimensions], dtype=np.int16)

            #update for every literal in solution
            [self.update_with_literal(x) for x in self.solution]
            self.reset_board = False
    
        #last step: update new literal
        self.update_with_literal(literal=literal)
        return
        

    def block_ranges(self, block):
        if self.dimensions == 4:
            #find position ranges of this block of 4x4 sodoku
            (rx, ry, cx, cy) = self.fourxfour_block_ranges.get(block,"Invalid input")

        elif self.dimensions == 9:
            #find position ranges of this block of 9x9 sodoku
            (rx, ry, cx, cy) = self.ninexnine_block_ranges.get(block,"Invalid input")
        return (rx, ry, cx, cy)

    def elements_in_block(self, block)->list: #list with all values from block
        
        #find ranges of corresponding block
        (rx, ry, cx, cy) = self.block_ranges(block)
        
        #return its values (as flat array)
        result = self.board_rep[rx:ry, cx:cy].flatten()
        return result


    def find_literal_from_position(self, r, c):
        #range of options:
        options = [x for x in range(1, self.dimensions+1)]
        #find values in same row and except them from options
        after_row_options = [x for x in options if x not in self.board_rep[r]]

        #find values in same column and except them from options
        after_column_options = [x for x in after_row_options if x not in self.board_rep[:,c]]
        
        #find values in same block
        values_in_block = self.elements_in_block(block=self.find_block(r, c))
        # except the block values from options
        final_options = [x for x in after_column_options if x not in values_in_block]

        #if no options are available, return False
        if len(final_options)==0:
            return False

        # suggest a value and create literal
        val = final_options[0] #random.choice(final_options)
        literal = int(f'{r+1}{c+1}{val}')

        #check if literal is not allready tried before backpropagation
        while -1*literal in self.solution:
            # if so, remove value from options
            final_options = [x for x in final_options if x != val]

            #if no options are available, return False
            if len(final_options)==0:
                return False

            # pick new value and create new literal
            val = random.choice(final_options)
            literal = int(f'{r+1}{c+1}{val}')

        # return 
        return literal


    def find_max_info_position(self):
        #find index of the flattend matrix with most information points
        highest = self.info_matrix.argmax()

        #transform to row and column
        row = int(highest / self.dimensions) 
        col =  highest % self.dimensions 
        return row, col

    def dpll(self, knowledge_base):
        self.step += 1

        #check for unit clauses
        litteral = self.has_unit_clause(knowledge_base)
        
        while litteral:
            if litteral > 0:
                v_print('Unit clause: ' + str(litteral))
            #propagate kb by making unit clause true
            knowledge_base = self.unit_propagation(knowledge_base, litteral)
            #check for more unit clauses
            litteral = self.has_unit_clause(knowledge_base)
        
        if visualise:
            #visualise current sudoku
            vs.visualizer(solution=self.solution)

        #Check if there are no clauses left
        if knowledge_base == []:
            return True
        
        #Check for empty clause
        for clause in knowledge_base:
            if len(clause) == 0:
                return False

        #choose a litteral to propagate
        litteral = self.choose_litteral(knowledge_base)
        
        # if there is no possible litteral found for a position, return false
        if not litteral:
            return False

        if self.dpll(knowledge_base + [[litteral]]):
            #return true if solution is found
            return True
        else:
            self.count_backpropagation += 1
            # v_print('BACKPROPAGATE: ' + str(litteral))
            #delete literal from solution that are added after invalid literal
            index = self.solution.index(litteral)
            self.solution = self.solution[:index]
            #reset board representation
            self.reset_board = True
            #propagate with negation of literal
            return self.dpll(knowledge_base + [[-1*litteral]])
        

def v_print(text):
    try:
        if verbose:
            print(text)
    except:
        pass

if __name__ == '__main__':
    # cnf = dpll.dpll_algorithm()
    # [knowledge_base] = sr.create_input('top91.sdk.txt', cnf_form=True, num_of_games=1)
    # knowledge_base = sr.create_input('top91.sdk.txt', cnf_form=True, num_of_games=91)
    # [knowledge_base] = sr.create_input('4x4.txt', cnf_form=True, num_of_games=1)
    knowledge_base = sr.create_input('4x4.txt', cnf_form=True, num_of_games=1000)
    verbose = False
    visualise = False
    start_time = datetime.now()

    total_data = []
    
    for kb in knowledge_base:  
        data = []    
        human = Human_intuition(dimensions=9)
        if human.dpll(kb):
            end_time = datetime.now()
            runtime = end_time - start_time
            data.append(runtime)
            computational_time = runtime - human.clean_up_time
            data.append(computational_time)
            data.append(human.count_backpropagation)
            print("\n\nsatisfiable\n")
            # print(f'\tunits: {cnf.count_units}\n\tchoices: {cnf.count_lit_choose}\n\tlayer: {cnf.layer}')
            # vs.visualizer(human.solution, dimensions=human.dimensions)
        else:
            print("\n\nunsatisfiable\n")
        total_data.append(data)
    # print(total_data)
    results = pd.DataFrame(total_data, columns=('Runtime', 'Computationaltime', 'Backtracks'))
    results.to_csv('results_human_in4x4.csv', index=False)