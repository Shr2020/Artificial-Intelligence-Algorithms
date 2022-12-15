## Objective

 Implement two programs:
 1. kNN
 2. kMeans.


## Running the program

Requirement: Python 3

Library used: numpy

### Running KNN 

```
usage: knn.py [-h] [-k K] [-unitw] -d D $train_file $test_file

positional arguments:
  train_file       specify the training file to be read
  test_file        specify the test file to be read

optional arguments:
  -h, --help       show this help message and exit
  -k K, --k K      k nearest neighbors
  -unitw, --unitw  whether to use unit voting weights. Default value is false. If not set then use (1/d)
  -d D, --d D      specify distance function to use, one of: euclidean squared "e2" (default)or manhattan "manh". Permissible value = e2/manh
```

Examples:

```
python3 knn.py -k 7 -d e2 -unitw train_3.csv test_3.csv
python3 knn.py -k 7 -d manh train_3.csv test_3.csv
python3 knn.py -d e2 train_3.csv test_3.csv

```

### Running KMEANS

```
usage: kmeans.py [-h] -data $input_file -d e2 0,0 200,200 500,500

positional arguments:
  centroids             specify the centroids

optional arguments:
  -h, --help            show this help message and exit
  -data DATA, --data DATA
                        file containing data
  -d D, --d D           specify the mode of distance calculation. Permissible value = e2/manh
```

Examples:

```
python3 kmeans.py -d manh -data kmeans_train2.csv 0,0,0 200,200,200 500,500,500
python3 kmeans.py -d e2 -data kmeans_train2.csv 0,0,0 200,200,200 500,500,500
python3 kmeans.py -d manh -data kmeans_train1.csv 0,0 200,200 500,500
python3 kmeans.py -d e2 -data kmeans_train1.csv 0,0 200,200 500,500

```

## Note:
- The permissible values of d is e2 or manh
- Default value of k is 3 if not set.
- Default value for unitw is false if not set.