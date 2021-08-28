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
```python jerboa.py {run/test} ...```<br/>
```python jerboa.py test {ext/int} ...```

### Optional Parameters
python jerboa.py (1) run (2)<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;test (3) ext (4)<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;int (5)
                              
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
	- ```-tsne``` - Use TSNE to display the training data on a 2D plot. <br/>
![tsne](https://user-images.githubusercontent.com/47477832/131218964-9297471f-bf1c-4020-9389-fc39ec708979.png)

(4):
- Positional:
	-  ```input_path``` - Location of input data.
	- ```expected_output``` - The string that was actually typed.
- Optional:
	- ```-simgraph``` - Display a graph of similarity scores for all values of K.<br/>
<img src="https://user-images.githubusercontent.com/47477832/131218967-a8c0d35d-eb33-4f46-a46e-d9d7f8fbf113.png" width="200">


(5):
- Optional:
	- ```-testprop TESTPROP``` - Set the proportion of samples used to test model. (Default: 0.1)
	- ```-kgraph``` - Display a graph showing the accuracy of each K-Value. <br/>
<img src="https://user-images.githubusercontent.com/47477832/131218970-a8cfb158-4173-4caa-bf6e-578e18830778.png" width="200">

## Arduino Sketch
This is the sketch used by the Arduino to catch the sounds made by the keypress and store them in the SD card for later processing.

### Libraries
- SD
- SPI

### Configuration
<img src="https://user-images.githubusercontent.com/47477832/131218397-335fdccc-a23c-4226-81c5-53f69ad96601.png" width="200">


## Data Visualisation
Processing sketch that displays the captured data. <br/>
![Processing](https://user-images.githubusercontent.com/47477832/131218971-49652dd3-d9ba-4cf2-8904-685e8b48dd23.png)
