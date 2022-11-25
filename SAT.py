import hulpfunctions as hf
import sudoku_reader as sr
import visualise_sudoku as vs

#algorithms
from human_intuition import Human_intuition
from dpll import dpll_algorithm
from AA_JW1 import jw_one_sided
from JW2 import jw_two_sided
from count_occurrence import new_dpll


import sys
from datetime import datetime
import pandas as pd


def read_input():
    #read what algorithm should be used
    try:
        algorithm_number = int(sys.argv[1])
    except:
        algorithm_number = 1

    try:
        #read filename
        filename = sys.argv[2]
    except:
        #use the 91 9x9's as default
        filename = 'top91.sdk.txt' 

    try:
        #try to retrieve num of games from input
        number_of_games = int(sys.argv[3])
    except:
        #use 1 if not possible
        number_of_games = 1
    
    try:
        visualiser = sys.argv[4] == "True"
    except:
        visualiser = False


    return algorithm_number, filename, number_of_games, visualiser


def which_algorithm(algo_num):
    algorithms = {
        1: dpll_algorithm(),
        2: Human_intuition(),
        3: new_dpll(), #count occurrences
        4: jw_one_sided(),
        5: jw_two_sided()
    }
    #find and return corresponding algorithm
    return algorithms.get(algo_num, "Invalid algorithm number input")



if __name__ == '__main__':
    #read input
    algorithm_number, filename, number_of_games, visualiser = read_input()

    #to store results
    total_data = []
    
    #timer of solving
    start_time = datetime.now()
    
    #create knowledge base(s) from inputed file
    knowledge_base = sr.create_input(filename=filename, cnf_form=True, num_of_games=number_of_games)

    for index, kb in enumerate(knowledge_base):
        #initiate algorithm
        solver = which_algorithm(algo_num=algorithm_number)

        #data per sudoku
        data = []
        
        #run solver
        if solver.dpll(kb):
            print("satisfiable")    
            if visualiser:
                vs.visualizer(solution=solver.solution)
        else:
            print("unsatisfiable")

        #timers
        end_time = datetime.now()
        runtime = end_time - start_time
        computational_time = runtime - solver.clean_up_time
        
        #store results
        data.append(runtime)
        data.append(computational_time)
        data.append(solver.count_backpropagation)
        total_data.append(data)

        #save results to csv every 5 sudoku's
        if index % 5 == 0:
            results = pd.DataFrame(total_data, columns=('Runtime', 'Computationaltime', 'Backtracks'))
            results.to_csv('results_basic_dpll.csv', index=False)

    #save final results
    results = pd.DataFrame(total_data, columns=('Runtime', 'Computationaltime', 'Backtracks'))
    results.to_csv(f'results.csv', index=False)

