from dpll import dpll_algorithm
import sudoku_reader as sr

class new_dpll(dpll_algorithm):
    def choose_litteral(self, knowledge_base):
        dict_kb = self.make_dictionary(knowledge_base)
        max_value = max(dict_kb, key=dict_kb.get)
        return(max_value)

    def make_dictionary(self, knowledge_base):
        dict_kb = {}

        for clause in knowledge_base:
            for litteral in clause:
                if litteral not in dict_kb:
                    dict_kb[litteral] = 1
                else:
                    dict_kb[litteral] += 1

        return(dict_kb)

if __name__ == '__main__':
    cnf = new_dpll()
    # knowledge_base = cnf.get_knowledge_base()
    [knowledge_base] = sr.create_input('4x4.txt', cnf_form=True, num_of_games=1)

    if cnf.dpll(knowledge_base):
        print("satisfiable")

    else:
        print("unsatisfiable")


