import datetime as dt
import os
# import new_neat.neat as neat
import copy
import pickle
import matplotlib.pyplot as plt
import numpy as np
import time
# import new_neat.neat.visualize as visualize


def define_parent_folder(test=True):
    if test:
        parent_folder = create_folder('test')
        # parent_folder = 'test/'
    else:
        parent_folder = create_folder('result')
    return parent_folder


def create_folder(name, add_date=False, now=dt.datetime.now()):

    #create name and folder of experiment named after the parameter choices
    if add_date:
        if not os.path.exists(name):
            os.mkdir(name)
        experiment_name = f'{name}/date_({now.month}-{now.day}-{now.hour}.{now.minute})'
    else:
        experiment_name = name

    if not os.path.exists(experiment_name):
        os.mkdir(experiment_name)

    #create path and folder for the saving of results
    return experiment_name

#easily create and/or append text to text files
def write_or_append_file(filename:str, text:str):
    if not os.path.exists(filename):
        #create and write file
        with open(filename, 'w') as f:
            f.write(text)
        f.close()
    else:
        #append to file
        with open(filename, 'a') as f:
            f.write(text)
        f.close()

def read_text_file(file_path):
    with open(file_path) as f:
        lines = f.readlines()
        f.close()
    return lines


def save_object(obj, filename_inc_extension:str):
    with open(filename_inc_extension, 'wb') as outp:  # Overwrites any existing file.
        pickle.dump(obj, outp, pickle.HIGHEST_PROTOCOL)
    return


def save_model_as_object(model, filename_no_extension:str, path:str=''):
    model_to_save = copy.copy(model)

    if path:
        path = path + '/'
    save_object(model_to_save, f'{path}{filename_no_extension}.pkl')
    return

def pickle_loader(filename_inc_extension):
    """ Deserialize a file of pickled objects. """
    with open(filename_inc_extension, "rb") as f:
        while True:
            try:
                yield pickle.load(f)
            except EOFError:
                break


def normalize(value, max, min):
    return (value - min) / (max - min)



class Timer:
    def __init__(self):
        self._start_time = None

    def start(self):
        """Start a new timer"""
        if self._start_time is not None:
            print(f"Timer is running. Use .stop() to stop it")

        self._start_time = time.perf_counter()

    def stop(self)->float:
        """Stop the timer, and report the elapsed time"""
        if self._start_time is None:
            print(f"Timer is not running. Use .start() to start it")

        elapsed_time = time.perf_counter() - self._start_time
        self._start_time = None
        # print(f"Elapsed time: {elapsed_time:0.4f} seconds")    
        return round(elapsed_time, 5)

class print_verbose:
    def __init__(self, accept_verbose_from=0, start_time:dt.datetime=dt.datetime.now()) -> None:
        self.accept_verbose_from = accept_verbose_from
        self.start_time = f'({start_time.month}-{start_time.day}-{start_time.hour}.{start_time.minute})'

    def nt(self, text, verbose_level_of_text=0, not_if_zero=False):
        if verbose_level_of_text >= self.accept_verbose_from:
            if not_if_zero and self.accept_verbose_from == 0:
                pass
            else:
                print(text)
