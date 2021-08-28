
# Jerboa
Arduino-based acoustic keylogger utilising a KNN model to guess key presses based on its provided training data.

## Program
This program can guess keys pressed in input data, test the model on external data, and also test models on a subset of its training data.

### Example Usage
Use training data to create model and guess keys pressed in recorded data stored in file "test_data/hello.txt":
``` python jerboa.py run "test_data/hello.txt" ```

Use training data to create model and test how well model performs on the data in "test_data/hello.txt" where you typed "helloiamjerboa":
``` python jerboa.py test ext "test_data/hello.txt" "helloiamjerboa" ```

Use training data to create model and test how well model performs a subset of the provided training data:
``` python jerboa.py test int ```

### Definitions
- *Strict Similarity* - Correct guesses, i.e. The model guessed X% of the characters correctly where X is the strict similarity.
- *Weak Similarity* - Strict Similarity + Incorrect Guess but the correct character had a non-zero probability.

### Parser Structure
```python jerboa.py {run/test} ...```
```python jerboa.py test {ext/int} ...```

### Optional Parameters
python jerboa.py (1) run (2)
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;test (3) ext (4)
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;int (5)
                              
(1):
- Positional:
	-  ```{run/test}```
- Optional:
	- ```-metric``` {manhattan,euclidian,chebyshev,canberra,braycurtis} - Metric to be used in the model. (Default: 'braycurtis')
	- ```-weight``` {distance, uniform} - Weight function to use in prediction. (Default: 'distance')
	- ```-points POINTS``` - Number of points from start to use from imported data. (Default: 200)

(2): 
- Positional:
	-  ```input_path``` - Location of input data.

(3): 
- Positional:
	-  ```{ext/int}``` - Type of test to perform.
- Optional:
	- ```start_k START_K``` - The first K value in the range to test.
	- ```end_k END_K``` - The last K value in the range to test.
	- ```-a``` - Display all non-zero probability possiblities for each character guess.
	- ```-tsne``` - Use TSNE to display the training data on a 2D plot.

(4):
- Positional:
	-  ```input_path``` - Location of input data.
	- ```expected_output``` - The string that was actually typed.
- Optional:
	- ```-simgraph``` - Display a graph of similarity scores for all values of K.

(5):
- Optional:
	- ```-kgraph``` - Display a graph showing the accuracy of each K-Value.
	- ```-testprop TESTPROP``` - Set the proportion of samples used to test model. (Default: 0.1)

## Arduino Sketch

## Data Visualisation
