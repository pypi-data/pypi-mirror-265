import copy
import os
import numpy as np
from scipy import interpolate
import math

def get_bound_input_from_user(text):
    """ this functions asks user to input single number and returns it"""
    while True:
        print(text)
        inputted = get_user_input()
        if type(inputted) != str:
            return inputted
        else:
            print("Wrong input! Try again!")


def ask_yes_no_question(question):
    """ this function asks user QUESTION, waits for the input, returns True or False for Y or N """
    while True:
        print(question + " (y/n) ")
        answer = get_user_input()

        if type(answer) == str:
            if answer == "y":
                return True
            elif answer == "n":
                return False
            else:
                print("Wrong input (y/n)!")
        else:
            print("Wrong input (y/n)!")


def get_user_input():
    """ this function gets input from a user """
    inputted = input()

    try:
        inputted = int(inputted)
        return inputted
    except ValueError:
        try:
            inputted = float(inputted)
            return input
        except ValueError:
            inputted = str(inputted)
            return inputted


def load_multicolumn_data_from_file(file, delimiter="\t", X_column=0):
    """ loads raw data vectors from file and
    returns tuple of data vectors with common X vector ([name1, X, Y1], [name2, X, Y2], ... [namen, X, Yn]) vectors and filename"""
    """ file is entire path to file """
    filename = os.path.basename(file)
    set = []
    try:
        with open(file) as f:
            file_lines = f.readlines()
            column_count = len(file_lines[0].split(delimiter))
            #print(column_count)

            X = [line.split(delimiter)[X_column] for line in file_lines[1:]]
            X = [float(x.replace(",", ".")) for x in X]
            #X = [float(x) for x in X]

            for i in range(1+X_column, column_count):
                name = file_lines[0].split(delimiter)[i]
                #print("Loading vector: " + name)
                Y = [line.split(delimiter)[i] for line in file_lines[1:]]
                try:
                    Y = [float(y.replace(",", ".")) for y in Y]
                    for idx, val in enumerate(Y):
                        if math.isnan(val):
                            if idx == 0:
                                Y[idx] = 0
                            else:
                                Y[idx] = Y[idx-1]
                except ValueError:
                    Y = [0 for y in Y]
                # Y = [float(y) for y in Y]
                vec = (name, X, Y)
                set.append(vec)

    except FileNotFoundError:
        print("Error: Input file is missing.")
        return -1

    #print("Loaded file: " + filename)
    return set

def load_data_from_file(file, source="NI"):
    """ loads raw data from file and returns X, Y vectors and filename"""
    """ file is entire path to file """
    filename = os.path.basename(file)

    try:
        with open(file) as f:

            file_lines = f.readlines()
            file_lines = [check_decimal_separator(line) for line in file_lines[1:]]
            if check_if_szafa_file(file_lines[1]):
                source = "SZAFA"

        if source == "SZAFA":
            X = [line.split(",")[0] for line in file_lines[1:]]
            X = [float(x.replace("ns", "")) / 1000000000 for x in X]
            Y = [line.split(",")[1] for line in file_lines[1:]]
            Y = [float(y.replace("\n", "")) for y in Y]
        elif source == "NI":
            X = [line.split("\t")[0] for line in file_lines[1:]]
            X = [float(x) for x in X]
            Y = [line.split("\t")[1] for line in file_lines[1:]]
            Y = [float(y) for y in Y]
        else:
            X = [line.split(",")[0] for line in file_lines[1:]]
            X = [float(x) for x in X]
            Y = [line.split(",")[1] for line in file_lines[1:]]
            Y = [float(y) for y in Y]

    except FileNotFoundError:
        print("Error: Input file is missing.")
        return -1

    #print("Loaded file: " + filename)
    return X, Y, filename


def load_filepaths_from_folder(folder_name):
    """ this function returns all filepaths in the folder_name relative to the scripts directory """
    dir = os.getcwd()
    dir = dir + "/" + folder_name
    filenames = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]
    
    for idx, val in enumerate(filenames):
        if ".md" not in val and ".csv" not in val and ".txt" not in val:
            filenames.pop(idx)

    filepaths = [dir + "/" + f for f in filenames]

    return filepaths


def load_filenames_from_folder(folder_name):
    """ this function reads all filenames in the folder_name relative to the scripts directory """
    dir = os.getcwd()
    dir = dir + "/" + folder_name
    filenames = os.listdir(dir)

    return filenames

def get_path_to_file(folder_name, file_name):
    """ this function returns full path to the file given the relative folder and name of the file """
    dir = os.getcwd()
    dir = dir + "/" + folder_name + "/" + file_name
    return dir


def interpolate_data(x, y, samples=1000, x_vector=[]):
    interp_data = interpolate.interp1d(x, y, kind="linear")
    if x_vector is []:
        x_vector = np.linspace(x[0], x[-1], samples)
    output = interp_data(x_vector)
    return x_vector, output


def trim_data(X, Y, lower_bound, upper_bound):
    """przycina wektory X i Y od lower bound do upper bound"""

    start_index = X.index((min(X, key=lambda x: abs(x - lower_bound))))
    stop_index = X.index((min(X, key=lambda x: abs(x - upper_bound))))

    x_new = X[start_index:stop_index]
    y_new = Y[start_index:stop_index]

    return x_new, y_new


def check_decimal_separator(line):
    count = line.count(",")
    if count > 1:
        line.replace(",", ".")
        idx = line.find(",")
        line = list(line)
        line[idx] = ","
        line = "".join(line)
    return line


def check_if_szafa_file(line):
    count = line.count("ns")
    if count > 0:
        return True
    else:
        return False


def fix_remove_zeros(X, Y):
    x2 = []
    y2 = []
    for i in range(len(X)):
        if X[i] > 0.05:
            x2.append(X[i])
            y2.append(Y[i])

    return x2, y2


def fix_remove_outliers(X, Y, bound_X):
    x2 = []
    y2 = []
    for i in range(len(X)):
        if X[i] < bound_X:
            x2.append(X[i])
            y2.append(Y[i])

    return x2, y2


def fix_remove_from_area(X, Y, x1, x2, y1, y2):
    X2 = []
    Y2 = []
    for i in range(len(X)):
        ok = True
        if x1 < X[i] < x2 and y1 < Y[i] < y2:
            ok = False
        if ok:
            X2.append(X[i])
            Y2.append(Y[i])

    return X2, Y2