from JW1 import jw_one_sided
import sudoku_reader as sr

class jw_two_sided(jw_one_sided):
    def choose_litteral(self, knowledge_base):
        dicts = self.calculate_j(knowledge_base)
        dict_j = dicts[0]
        dict_jw02 = dicts[1]
        max_value = max(dict_jw02, key=dict_jw02.get)
        if -1*max_value in dict_j:
            if dict_j[max_value] > dict_j[-1*max_value]:
                return(max_value)
            else:
                return(-1*max_value)
        else:
            return(max_value)

       
    def calculate_j(self, knowledge_base):
        dict_j_values = {}
        dict_kb = self.make_dictionary(knowledge_base)

        for litteral in dict_kb:
            j = []
            for lenghts in dict_kb[litteral]:
                calculate_j = 2 ** (-1*lenghts)
                j.append(calculate_j)
            dict_j_values[litteral] = sum(j)

        jw02 = {}
        for litteral in dict_j_values:
            jw02[litteral] = dict_j_values[litteral]
            if -1*litteral in dict_j_values:
                jw02[litteral] += dict_j_values[-1*litteral]


        return(dict_j_values, jw02)

if __name__ == '__main__':
    cnf = jw_two_sided()
    # knowledge_base = cnf.get_knowledge_base()
    [knowledge_base] = sr.create_input('4x4.txt', cnf_form=True, num_of_games=1)

    if cnf.dpll(knowledge_base):
        print("satisfiable")

    else:
        print("unsatisfiable")

