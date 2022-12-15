## Objective

Implement a program that, using the selected algorithm, finds a path in a graph from a start to goal vertex.

###  Algorithms
Implement 3 algorithms:
1. **Breadth First Search** using a visited list to avoid duplicate vertices (nodes should be visited in alphabetical order)
2. **Iterative Deepening**, using the -depth parameter for initial depth, then increasing by 1. (You may also use a visited list: not required) (nodes should be visited in alphabetical order)
3. **A-star**, using an h function of Euclidean distance from potential expansion node to goal.


## Running the program

Requirement: Python 3

```
usage: driver.py [-h] [-v] -start START -end END -algo ALGO [-depth DEPTH] filename

positional arguments:
  filename              specify the input file to be read

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         increase output verbosity
  -start START, --start START
                        specify the starting node
  -end END, --end END   specify the ending node
  -algo ALGO, --algo ALGO
                        specify the algorithm to use. Permissible values = BFS, ID, A_star
  -depth DEPTH, --depth DEPTH
                        depth for iterative deepening

```

Examples:

```
python3 driver.py -start S -end G -algo bfs ex1.txt
python3 driver.py -start S -end G -algo a_star ex1.txt
python3 driver.py -start S -end G -algo id -depth 1 ex1.txt
```

## Note:
- The permissible values of algo are:
  - `bfs` (for breadth first search),
  - `a_star` (for A*),
  - `id` (for iterative deepening)
- For iterative deepening default depth paramater is 2. To change the depth add `-depth $depth` in the command.
