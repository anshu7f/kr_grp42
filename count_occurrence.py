from dpll import dpll_algorithm
import sudoku_reader as sr
import random
import sudoku_reader as sr
import visualise_sudoku as vs
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

class new_dpll(dpll_algorithm):
    def choose_litteral(self, knowledge_base):
        dict_kb = self.make_dictionary(knowledge_base)
        max_value = min(dict_kb, key=dict_kb.get)
        # print(max_value)
        return(max_value)

    def make_dictionary(self, knowledge_base):
        dict_kb = {}

        for clause in knowledge_base:
            for litteral in clause:
                if litteral not in dict_kb:
                    dict_kb[litteral] = 1
                else:
                    dict_kb[litteral] += 1
        # print(dict_kb)
        return(dict_kb)

if __name__ == '__main__':

    # knowledge_base = cnf.get_knowledge_base()
    start_time = datetime.now()
    knowledge_base = sr.create_input('top91.sdk.txt', cnf_form=True, num_of_games=91)
    # knowledge_base = sr.create_input('4x4.txt', cnf_form=True, num_of_games=1000)
    total_data = []
    

    for kb in knowledge_base:
        cnf = new_dpll()  
        data = []
        if cnf.dpll(kb):
            end_time = datetime.now()
            runtime = end_time - start_time
            data.append(runtime)
            computational_time = runtime - cnf.clean_up_time
            data.append(computational_time)
            data.append(cnf.count_backpropagation)

            print("satisfiable")
            # print('Duration: {}'.format(runtime))
            # print('computational time: {}'.format(computational_time))
            # print(cnf.count_backpropagation)
            # print(f'\tunits: {cnf.count_units}\n\tchoices: {cnf.count_lit_choose}\n\tlayer: {cnf.layer}')
            # vs.visualizer(cnf.solution)
    
            
        else:
            print("unsatisfiable")

        total_data.append(data)
   
    results = pd.DataFrame(total_data, columns=('Runtime', 'Computationaltime', 'Backtracks'))
    results.to_csv('results_dpll_literal_occurrence_9x9_min.csv', index=False)


