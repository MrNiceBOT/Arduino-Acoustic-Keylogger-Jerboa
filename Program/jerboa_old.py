# Import libraries
import sklearn
from sklearn.neighbors import KNeighborsClassifier
from scipy.fft import fft, fftfreq
import numpy as np
import argparse

# Loads training data from the passed file into the passed arrays
def load_training(file_name, target_val, training_data, training_targets, 
    elements):
    # Convert file string to integer arrays
    file = open(file_name, "r")

    while True:
        chunk = file.readline();
        if(chunk == ''):
            break

        list = chunk.split(' ')

        j = len(list) -1
        while((list[j] == '') | (list[j] == '\n')):
            j-=1
            list.pop()

        training_targets.append(target_val)

        list = [int(i) for i in list] # Convert to array of integers

        ret = []
        for i in range(0, elements):
            ret.append(int(list[i]))

        training_data.append([i.real for i in fft(ret)])

# Loads the input file to be fed to the model
def load_input(file_name, elements):
    input_file = open(file_name)
    input_data = []

    while True:
        chunk = input_file.readline();
        if(chunk == ''):
            break

        list = chunk.split(' ')

        j = len(list) -1
        while((list[j] == '') | (list[j] == '\n')):
            j-=1
            list.pop()

        list = [int(i) for i in list] # Convert to array of integers

        ret = []
        for i in range(0, elements):
            ret.append(int(list[i]))

        input_data.append([i.real for i in fft(ret)])

    return input_data

def main(args):
    # Dataset variables
    training_data = []
    training_targets = []

    # The characters being guessed from
    characters = []

    # Load data files and respective ascii labels
    for i in range(97, 123):
        load_training("data/" + chr(i) + ".txt", i, training_data, 
            training_targets, 200)
        characters.append(chr(i))

    # load input data
    input_data = load_input(args.Input, 200)

    # Generate dataset
    data_set = \
        sklearn.utils.Bunch(data = np.asarray(training_data), 
            target = np.asarray(training_targets))

    # Train and test the KNN for various k's
    k_vals = [1, 4, 7, 10, 13, 16, 19, 22, 25]

    for k in k_vals:
        # Print predicted text entry
        knn = KNeighborsClassifier(n_neighbors=k, 
            weights = 'distance', metric=args.m)
        
        knn.fit(training_data, training_targets)

        # Get predictions for input data and probability
        prediction = knn.predict(input_data)
        probabilities = knn.predict_proba(input_data)

        predicted_string = ""
        for i in prediction:
            predicted_string = predicted_string + chr(i)
        
        print("K =", k, '\t', predicted_string)

if __name__ == "__main__":
    print("""
      /-\                /-\                    
     |---\              /---|                  
     |----|            |----|           ###      
      \----\          /----/           #####       
        \---|        |---/            #######             
          \-\________/-/              #######         
         /    \    /    \  ________     ####        
        /     *    *     \/ ______ \     \ \       
       |        ..        |/      \ \    / /   
        \      \__/      /        / /    \ \      
       $$$\_ ________ _/$$$       \ \____/ /   
       \  \ |        | /  /        \______/        
         \_\|        |/_/                     
 _______ _______ _______ _______ _______ _______ 
|\     /|\     /|\     /|\     /|\     /|\     /|
| +---+ | +---+ | +---+ | +---+ | +---+ | +---+ |
| | J | | | E | | | R | | | B | | | O | | | A | |
| +---+ | +---+ | +---+ | +---+ | +---+ | +---+ |
|/_____\|/_____\|/_____\|/_____\|/_____\|/_____\|
""")

    # Set up argument parser
    parser = argparse.ArgumentParser("python jerboa.py")

    parser.add_argument("Input", type=str, 
        help = "Location of input data.")

    parser.add_argument('-m', type=str, default='braycurtis', 
        help = "Metric to be used in the model. (Default: 'braycurtis')", 
        choices = ['manhattan', 'euclidian', 'chebyshev', 'canberra', 'braycurtis'])
    parser.add_argument('-w', type=str, default='distance', 
        help = "Weight function to use in prediction. (Default: 'distance')",
        choices = ['distance', 'uniform'])

    args = parser.parse_args()

    main(args)
