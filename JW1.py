from dpll import dpll_algorithm
import sudoku_reader as sr

class jw_one_sided(dpll_algorithm):
    def choose_litteral(self, knowledge_base):
        dict_j_values = self.calculate_j(knowledge_base)
        max_value = max(dict_j_values, key=dict_j_values.get)
        return(max_value)

    def make_dictionary(self, knowledge_base):
        dict_kb = {}

        for clause in knowledge_base:
            for litteral in clause:
                if litteral not in dict_kb:
                    dict_kb[litteral] = [len(clause)]
                else:
                    dict_kb[litteral].append(len(clause))

        return(dict_kb)

    def calculate_j(self, knowledge_base):
        dict_j_values = {}
        dict_kb = self.make_dictionary(knowledge_base)

        for litteral in dict_kb:
            j = []
            for lenghts in dict_kb[litteral]:
                calculate_j = 2 ** (-1*lenghts)
                j.append(calculate_j)
            dict_j_values[litteral] = sum(j)
        return(dict_j_values)

if __name__ == '__main__':
    cnf = jw_one_sided()
    # knowledge_base = cnf.get_knowledge_base()
    [knowledge_base] = sr.create_input('4x4.txt', cnf_form=True, num_of_games=1)

    if cnf.dpll(knowledge_base):
        print("satisfiable")

    else:
        print("unsatisfiable")
