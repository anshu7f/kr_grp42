import random
import sudoku_reader as sr
import visualise_sudoku as vs

class dpll_algorithm:
    def __init__(self):
        self.solution = []
        self.count_units = 0
        self.count_lit_choose = 0
        self.layer = 0
        # self.unit_propagations_this_layer = 0

    def add_start_to_solution(self, knowledge_base):
        litteral = self.has_unit_clause(knowledge_base)
        while litteral:
            self.solution.append(litteral)
            knowledge_base = self.unit_propagation(knowledge_base, litteral)
            litteral = self.has_unit_clause(knowledge_base)
        return True

        
    def get_knowledge_base(self):
        with open('sudoku1.cnf', 'r') as dimacs_file:
            lines = dimacs_file.readlines()

        knowledge_base = []

        for line in lines:
            line = line.strip()
            if len(line) > 0 \
                and not line.startswith('p') and not line.startswith('c'):
                knowledge_base.append([int(x) for x in line.split()[:-1]])
        return knowledge_base


    def has_unit_clause(self, knowledge_base):
        for clause in knowledge_base:
            if len(clause) == 1:
                self.solution.append(clause[0])
                return clause[0]
        return False


    def unit_propagation(self, knowledge_base, litteral):
        knowledge_base = [[l for l in clause if l != -1*litteral] for clause in knowledge_base if litteral not in clause]
        self.count_units += 1
        # self.unit_propagations_this_layer += 1
        return knowledge_base


    def choose_litteral(self, knowledge_base):
        # random_clause = random.choice(knowledge_base)
        # random_literal = random.choice(random_clause)
        self.count_lit_choose += 1
        return knowledge_base[0][0]


    def dpll(self, knowledge_base):
        self.layer =+ 1
        # unit_propagations_this_layer = 0

        litteral = self.has_unit_clause(knowledge_base)
        
        while litteral:
            # unit_propagations_this_layer += 1
            knowledge_base = self.unit_propagation(knowledge_base, litteral)
            litteral = self.has_unit_clause(knowledge_base)

        #Check if there are no clauses left
        if knowledge_base == []:
            return True
        
        #Check for empty clause
        for clause in knowledge_base:
            if len(clause) == 0:
                return False

        litteral = self.choose_litteral(knowledge_base)

        if self.dpll(knowledge_base + [[litteral]]):
            return True
        else:
            self.layer =+ 1
            index = self.solution.index(litteral)
            self.solution = self.solution[:index]
            return self.dpll(knowledge_base + [[-1*litteral]])
        

if __name__ == '__main__':
    # knowledge_base = cnf.get_knowledge_base()
    knowledge_base = sr.create_input('top91.sdk.txt', cnf_form=True, num_of_games=4)
    # knowledge_base = sr.create_input('4x4.txt', cnf_form=True, num_of_games=5)

    for kb in knowledge_base:
        cnf = dpll_algorithm()  
        
        if cnf.dpll(kb):
            print("satisfiable")
            # print(f'\tunits: {cnf.count_units}\n\tchoices: {cnf.count_lit_choose}\n\tlayer: {cnf.layer}')
            vs.visualizer(cnf.solution)
        else:
            print("unsatisfiable")
