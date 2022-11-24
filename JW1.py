from dpll import dpll_algorithm
import sudoku_reader as sr
import pandas as pd
from datetime import datetime, timedelta

class jw_one_sided(dpll_algorithm):
    def choose_litteral(self, knowledge_base):
        dict_j_values = self.calculate_j(knowledge_base)
        max_value = max(dict_j_values, key=dict_j_values.get)
        # print(max_value)
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
     # knowledge_base = cnf.get_knowledge_base()
    start_time = datetime.now()
    knowledge_base = sr.create_input('top91.sdk.txt', cnf_form=True, num_of_games=4)
    # knowledge_base = sr.create_input('4x4.txt', cnf_form=True, num_of_games=1000)
    total_data = []
    

    for index, kb in enumerate(knowledge_base):
        cnf = jw_one_sided() 
        data = []
        if cnf.dpll(kb):
            end_time = datetime.now()
            runtime = end_time - start_time
            data.append(runtime)
            computational_time = runtime - cnf.clean_up_time
            data.append(computational_time)
            data.append(cnf.count_backpropagation)

            print("satisfiable")    
            
        else:
            end_time = datetime.now()
            runtime = end_time - start_time
            data.append(runtime)
            computational_time = runtime - cnf.clean_up_time
            data.append(computational_time)
            data.append(cnf.count_backpropagation)

            print("unsatisfiable")

        total_data.append(data)

        if index % 5 == 0:
            #save results every 5 sudokus
            results = pd.DataFrame(total_data, columns=('Runtime', 'Computationaltime', 'Backtracks'))
            results.to_csv('results_JW1.csv', index=False)


    print(total_data)
    results = pd.DataFrame(total_data, columns=('Runtime', 'Computationaltime', 'Backtracks'))
    results.to_csv('results_JW19x9.csv', index=False)