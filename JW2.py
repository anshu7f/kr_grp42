from JW1 import jw_one_sided
import sudoku_reader as sr
import pandas as pd
from datetime import datetime, timedelta

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
     # knowledge_base = cnf.get_knowledge_base()
    start_time = datetime.now()
    knowledge_base = sr.create_input('top91.sdk.txt', cnf_form=True, num_of_games=4)
    # knowledge_base = sr.create_input('4x4.txt', cnf_form=True, num_of_games=1000)
    total_data = []
    

    for index, kb in enumerate(knowledge_base):
        cnf = jw_two_sided() 
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
            results.to_csv('results_JW2.csv', index=False)


    print(total_data)
    results = pd.DataFrame(total_data, columns=('Runtime', 'Computationaltime', 'Backtracks'))
    results.to_csv('results_JW29x9.csv', index=False)

