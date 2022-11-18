import random
import sudoku_reader as sr

class dpll_algorithm:
    def __init__(self):
        self.solution = []
        
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
        return knowledge_base


    def choose_litteral(self, knowledge_base):
        # random_clause = random.choice(knowledge_base)
        # random_literal = random.choice(random_clause)
        return knowledge_base[0][0]

    def check_pure_litteral(self, knowledge_base):
        dict_kb = {}

        for clause in knowledge_base:
            for litteral in clause:
                if litteral not in dict_kb:
                    dict_kb[litteral] = 1
                else:
                    dict_kb[litteral] += 1
        # return(dict_kb)
        pure_litterals = []
        for litteral in dict_kb.keys():
            if -1*litteral not in dict_kb.keys():
                pure_litterals.append(litteral)

        if len(pure_litterals)>0:
            return pure_litterals
        else:
            return False


    def dpll(self, knowledge_base):
        litteral = self.has_unit_clause(knowledge_base)
        
        while litteral:
            knowledge_base = self.unit_propagation(knowledge_base, litteral)
            litteral = self.has_unit_clause(knowledge_base)
        print(self.check_pure_litteral(knowledge_base))
        #Check if there are no clauses left
        if knowledge_base == []:
            return True
        
        #Check for empty clause
        for clause in knowledge_base:
            if len(clause) == 0:
                return False

        litteral = self.choose_litteral(knowledge_base)

        if self.dpll(knowledge_base + [[-1*litteral]]):
            return True
        return self.dpll(knowledge_base + [[litteral]])

if __name__ == '__main__':
    cnf = dpll_algorithm()
    # knowledge_base = cnf.get_knowledge_base()
    [knowledge_base] = sr.create_input('top91.sdk.txt', cnf_form=True, num_of_games=1)
    # test = cnf.check_pure_litteral(knowledge_base)
    # print(test)
    cnf.dpll(knowledge_base)
    # if cnf.dpll(knowledge_base):
    #     print("satisfiable")

    # else:
    #     print("unsatisfiable")