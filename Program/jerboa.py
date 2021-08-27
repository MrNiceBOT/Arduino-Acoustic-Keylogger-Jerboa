import sklearn
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn import metrics
from scipy.fft import fft, fftfreq
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import argparse
from sklearn.manifold import TSNE

def main(args):
    training_data = []
    training_targets = []

    # The characters being guessed from
    characters = []

    # Load data files and respective ascii labels
    for i in range(97, 123):
        load_training("data/" + chr(i) + ".txt", i, training_data, 
            training_targets, args.points)
        characters.append(chr(i))

    # Generate dataset
    data_set = \
        sklearn.utils.Bunch(data = np.asarray(training_data), 
            target = np.asarray(training_targets))

    if args.run_or_test == 'run':
        # load input data
        input_data = load_input(args.input_path, 200)

        # Train and test the KNN for various k's
        k_vals = [1, 4, 7, 10, 13, 16, 19, 22, 25]

        for k in k_vals:
            # Print predicted text entry
            knn = KNeighborsClassifier(n_neighbors=k, 
                weights = 'distance', metric=args.metric)
            
            knn.fit(training_data, training_targets)

            # Get predictions for input data and probability
            prediction = knn.predict(input_data)
            probabilities = knn.predict_proba(input_data)

            predicted_string = ""
            for i in prediction:
                predicted_string = predicted_string + chr(i)
            
            print("K =", k, '\t', predicted_string)
    elif args.run_or_test == 'test':
        # If tsne flag detected, plot tsne projection of training data
        if args.tsne:
            # Set plot colours to distinguish clusters easier
            mpl.rcParams['axes.prop_cycle'] = mpl.cycler(color=["tab:orange", 
            "tab:green", "tab:red", "tab:blue", "tab:purple", "tab:brown", 
            "tab:pink", "tab:gray", "tab:olive", "tab:cyan", "khaki", 
            "paleturquoise", "teal", "lightsalmon", "darkseagreen", "slategray", 
            "black", "yellow", "lime", "maroon", "silver", "magenta", "aqua", 
            "peru", "olive", "deepskyblue"]) 

            tsne_em = TSNE(n_components=2, perplexity=30, n_iter=1000, 
                verbose=1).fit_transform(training_data)

            x_min, x_max = np.min(tsne_em, 0), np.max(tsne_em, 0)
            data = (tsne_em - x_min) / (x_max - x_min)

            for i in range(int(data.shape[0]/250)):
                x = []
                y = []

                for j in range(250):
                    x.append(data[(i*250)+j, 0])
                    y.append(data[(i*250)+j, 1])

                plt.scatter(x, y, label = chr(97+i), s=8)
            
            plt.legend()
            plt.show() 

        if args.test_type=='ext':
            # load input data
            input_data = load_input(args.input_path, args.points)

        if args.test_type=='int':
            # Split into testing and training
            data_train, data_test, target_train, target_test = \
                train_test_split(training_data, training_targets, 
                test_size = args.testprop)

        k_range = range(args.start_k, args.end_k)
        scores_list = []
        strict_similarities = []
        weak_similarities = []

        for k in k_range:
            print("\nK Value:\t\t", k)

            # Define model
            knn = KNeighborsClassifier(n_neighbors=k, 
                weights = args.weight, metric=args.metric)

            if args.test_type=='int':
                knn.fit(data_train, target_train)
                target_prediction = knn.predict(data_test)
                scores_list.append(metrics.accuracy_score(target_test, 
                    target_prediction))
                print("Accuracy:\t\t", metrics.accuracy_score(target_test, 
                    target_prediction))

            if args.test_type=='ext':
                # Print predicted text entry
                print("Expected:\t\t", args.expected_output)

                knn.fit(training_data, training_targets)
                prediction = knn.predict(input_data)
                probabilities = knn.predict_proba(input_data)

                predicted_string = ""
                search_space = 1

                j=0
                for i in prediction:
                    predicted_string = predicted_string + chr(i)

                    poss_count = 0
                    for prob in probabilities[j]:
                        if (prob != 0):
                            poss_count += 1
                    search_space *= poss_count
                    j+=1
                    
                # Print results
                print("Predicted:\t\t", predicted_string)
                print("Strict Similarity:\t", round(get_similarity(
                    args.expected_output, predicted_string, 
                    knn.predict_proba(input_data),  characters)[0], 2), '%')
                print("Weak Similarity:\t", round(get_similarity(
                    args.expected_output, predicted_string, 
                    knn.predict_proba(input_data), characters)[1], 2), '%')
                print("Search Space: \t\t", search_space)

                if args.a:
                    j=0
                    print()
                    for i in prediction:
                        print("Predicted: ", chr(i))
                        print("Expected: ", args.expected_output[j])
                        print("Possible:")

                        k = 0
                        for prob in probabilities[j]:
                            if (prob != 0):
                                print(characters[k], '[', prob, ']\n', end='')
                            k+=1
                        print("\n")
                        j+=1

                # Add to simgraph data if flag present
                if args.simgraph:
                    strict_similarities.append(get_similarity(args.expected_output, 
                        predicted_string, knn.predict_proba(input_data), 
                        characters)[0])
                    weak_similarities.append(get_similarity(args.expected_output, 
                        predicted_string, knn.predict_proba(input_data), 
                        characters)[1])

        if (args.test_type=='ext'): 
            if args.simgraph:
                # Similarity score plot
                plt.plot(k_range, weak_similarities, color='blue', 
                    label="Weak")
                plt.plot(k_range, strict_similarities, color='red', 
                    label="Strict")
                plt.legend(loc="upper left")
                plt.xlabel('K Value')
                plt.ylabel('% Similarity')
                plt.show()

        if (args.test_type=='int'):
            if args.kgraph:
                # Accuracy from test plot
                plt.plot(k_range, scores_list)
                plt.xlabel('K')
                plt.ylabel('Accuracy')
                plt.show()

def load_chunk(chunk, elements):
    """Loads the values from the passed chunk and splits them into an 
    array of integers.

    Keyword arguments:
    chunk -- Chunk to extract data from
    elements -- The number of elements from the start of the 
    list to add in each set
    """

    list = chunk.split(' ')

    j = len(list) -1
    while((list[j] == '') | (list[j] == '\n')):
        j -= 1
        list.pop()

    list = [int(i) for i in list]

    ret = []
    for i in range(0, elements):
        ret.append(int(list[i]))

    return ret

def load_training(file_name, target_val, training_data, training_targets, 
    elements):

    """Load training data from passed file into training arrays.

    Keyword arguments:
    file_name -- File name to extract data from
    target_val -- What key the data represents (a, b, c, etc)
    training_data -- Array of training data to add too
    training_targets -- Array of training targets to add too
    elements -- The number of elements from the start of the 
    list to add in each set
    """

    file = open(file_name, "r")

     # Iterate over file until empty line recieved
    while True:
        chunk = file.readline()

        if(chunk == ''):
            break

        ret = load_chunk(chunk, elements)

        training_targets.append(target_val)

        # Convert data to frequency domain using fft()
        training_data.append([i.real for i in fft(ret)])

def load_input(file_name, elements):
    """Loads the input file to be fed to the model.

    Keyword arguments:
    file_name -- File name to extract data from
    elements -- The number of elements from the start of the 
    list to add in each set
    """

    input_file = open(file_name)
    input_data = []

    while True:
        chunk = input_file.readline()

        if(chunk == ''):
            break
        
        ret = load_chunk(chunk, elements)

        # Convert data to frequency domain using fft()
        input_data.append([i.real for i in fft(ret)])

    return input_data

# Gets the strict and weak similarity between the passed strings
def get_similarity(string1, string2, probabilities, characters):
    """Gets the strict and weak similarities between 2 strings.

    Keyword arguments:
    string1 -- Input string
    string2 -- String to compare against
    probabilities -- List of probabilities from KNN model
    characters -- The list of possible characters
    """

    strict_counter = 0
    weak_counter = 0
    for i in range(0, len(string1)):
        if string1[i] == string2[i]:
            strict_counter+=1

        k = 0
        for prob in probabilities[i]:
            if ((prob != 0) & (string1[i] == characters[k])):
                weak_counter += 1
                break
            
            k+=1

    # Return list containing strict and weak probabilities
    return [(strict_counter / len(string1)) * 100, 
            (weak_counter / len(string1)) * 100]

if __name__ == "__main__":
    print("""
       _                  _
      /-\                /-\                    
     |---\              /---|                 
     |----|            |----|           ####      
      \----\          /----/          ########       
        \---|        |---/            ########             
          \-\________/-/              ########         
         /    \    /    \  ________     ####        
        /    (*)  (*)    \/ ______ \     \ \       
       |        ..        |/      \ \    / /   
        \      [__]      /        / /    \ \      
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
    parser = argparse.ArgumentParser("python jerboa_test.py")

    parser.add_argument('-metric', type=str, default='braycurtis', 
        help = "Metric to be used in the model. (Default: 'braycurtis')", 
        choices = ['manhattan', 'euclidian', 'chebyshev', 'canberra', 'braycurtis'])
    parser.add_argument('-weight', type=str, default='distance', 
        help = "Weight function to use in prediction. (Default: 'distance')",
        choices = ['distance', 'uniform'])
    parser.add_argument('-points', type=int, default=200, 
        help = "Number of points from start to take from data (Default: 200).")

    # Add subparser to determine if running or testing model
    run_or_test_parser = parser.add_subparsers(
        help='Run model or Test model.', dest='run_or_test')

    # Parser for running the program on some input data and guessing for various K
    run_parser = run_or_test_parser.add_parser('run', 
        help='Use to run model on parsed data.')
    run_parser.add_argument("input_path", type=str, 
        help = "Location of input data.")

    # Parser for testing the model
    test_parser = run_or_test_parser.add_parser('test', 
        help='Used to test the model')
    test_parser.add_argument("-start_k", type=int, 
        help = "The first K value in the range to test.", default=1)
    test_parser.add_argument("-end_k", type=int, 
        help = "The last K value in the range to test.", default=25)
    test_parser.add_argument('-a', action='store_true', 
        help = "Display all non-zero probability possiblities for each guess.")
    test_parser.add_argument('-tsne', action='store_true', 
        help = "Use T-SNE to display the training data on a plot.")

    # Add subparser to determine which type of test
    internal_or_external_test_parser = test_parser.add_subparsers(
        help='Testing types.', dest='test_type')

    # Parser for external test on file
    external_test_parser = internal_or_external_test_parser.add_parser('ext', 
        help='Use to test model \
    on data from a file and compare against actual string.')
    external_test_parser.add_argument("input_path", type=str, 
        help = "Location of input data.")
    external_test_parser.add_argument("expected_output", type=str, 
        help = "The string to compare against (expected output).")
    external_test_parser.add_argument('-simgraph', action='store_true', 
        help = "Display a graph of similarity scores for all values of K.")
    
    # Parser for internal test on training data
    internal_test_parser = internal_or_external_test_parser.add_parser('int', 
        help='Use to test model \
    on subset of training data.')
    internal_test_parser.add_argument('-kgraph', action='store_true', 
        help = "Display a graph showing the k value accuracy.")
    internal_test_parser.add_argument('-testprop', type=float, default=0.2, 
        help = "Set the proportion of samples used to test model (Default: 0.1).")

    args = parser.parse_args()

    main(args)
