# kr_grp42

### How to run
Run the SAT.py as follows in your commandline:
SAT.py <which_algorithm:int> <filename_of_puzzles:str> <number_of_sudokus:int> <visualiser:bool>

- which_algorithm should be an integer among the following options:
  - 1 = baseline dbll (Default)
  - 2 = dbll with human intuition
  - 3 = dbll with most occurances 
  - 4 = dbll with one-sided Jeroslow-Wang
  - 5 = dbll with two-sided Jeroslow-Wang
  
- filename_of_puzzles should be a string with one of the filenames where puzzles are stored. See the "Dataset" folder for options. (Default: "top91.sdk.txt". The program automatically detects the size of the sudokus, but is limited to a maximum of 9x9.
- number_of_sudokus should be an integer determining how many sudokus one would like to have solved. (Default: 1)
- visualiser should be a string with "True" one would like a visualiser. It will then print the final solution for each sudoku if one is found. If anything (including empty) else than "True", the visualiser is off. (Default: "False")

##### Please note that each argument is optional. However, if one would like to set a argument to a certain value, one must set the arguments before too.
