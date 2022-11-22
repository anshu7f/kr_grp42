
import numpy as np
import math
import random

from dpll import dpll_algorithm

import sudoku_reader as sr
import visualise_sudoku as vs


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

        self.test = 0


    def unit_propagation(self, knowledge_base, litteral):
        knowledge_base = [[l for l in clause if l != -1*litteral] for clause in knowledge_base if litteral not in clause]
        self.count_units += 1
        #update (information) for choosing litteral
        self.update_boards(litteral)
        return knowledge_base


    def choose_litteral(self, knowledge_base):
        self.count_lit_choose += 1
        row, col = self.find_max_info_position()
        literal = self.find_literal_from_position(r=row, c=col)

        #plus 1 for translation from index to row number
        print('suggest:', literal)

        return literal

    
    def find_block(self, r, c) -> str:
        if self.dimensions == 4:
            block = f'{int(r / 2)}{int(c / 2)}'
        elif self.dimensions == 9:
            block = f'{int(r / 3)}{int(c / 3)}'
        return block

    def block_update(self, r, c):
        block = self.find_block(r, c)    
        #to do: implement adding information points to correct positions regarding 
        return self.info_matrix


    def info_update(self, r_i, c_i):
        #add information points to all elements in corresponding row
        self.info_matrix[r_i] = self.info_matrix[r_i] + 1
        #add information points to all elements in corresponding colomn
        self.info_matrix[:, c_i] = self.info_matrix[:, c_i] + 1
        #add information points to all elements inside corresponding block
        self.info_matrix = self.block_update(r_i, c_i)

        #note that this position is locked (and therefore non interesting for determining next literal)
        self.info_matrix[r_i,c_i] = -10000
        return self.info_matrix

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
            self.info_matrix = np.zeros([self.dimensions, self.dimensions], dtype=np.int16)
            self.board_rep = np.zeros([self.dimensions, self.dimensions], dtype=np.int16)

            [self.update_with_literal(x) for x in self.solution]
            self.reset_board = False
        
        self.update_with_literal(literal=literal)

        return

    def elements_in_block(self, block)->list: #list with all values from block

        if block:
            return [] 

    def find_literal_from_position(self, r, c):
        #range of options:
        options = [x for x in range(1, self.dimensions+1)]
        #find values in same row
        after_row_options = [x for x in options if x not in self.board_rep[r]]
        #find values in same column
        after_column_options = [x for x in after_row_options if x not in self.board_rep[:,c]]
        
        #find values in same block
        block = self.find_block(r, c) 
        final_options = [x for x in after_column_options if x not in self.elements_in_block(block=block)]

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
        
        #visualise current sudoku
        vs.visualizer(solution=self.solution) if verbose else 0

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
            v_print('BACKPROPAGATE: ' + str(litteral))
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
    knowledge_base = sr.create_input('top91.sdk.txt', cnf_form=True, num_of_games=5)
    # [knowledge_base] = sr.create_input('4x4.txt', cnf_form=True, num_of_games=1)
    
    verbose = True

    for kb in knowledge_base:        
        human = Human_intuition(dimensions=9)
        if human.dpll(knowledge_base):
            print("satisfiable")
            # print(f'\tunits: {cnf.count_units}\n\tchoices: {cnf.count_lit_choose}\n\tlayer: {cnf.layer}')
            vs.visualizer(human.solution, dimensions=human.dimensions)
        else:
            print("unsatisfiable")

