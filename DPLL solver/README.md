## Objective

Implement a program with 3 modes:
1. A generic DPLL solver
2. A BNF to CNF converter
3. Takes BNF and solves it by running the above two steps

## Running the program

Requirement: Python 3

```
usage: Driver.py [-v] -mode $mode $filename

positional arguments:
  filename              specify the input file to be read

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         increase output verbosity
  -mode MODE, --mode MODE
                        specify the mode ("cnf", "dpll", "solver")
```

Examples:

```
python3 Driver.py -v -mode cnf in1.txt
python3 Driver.py -v -mode dpll in3.txt
python3 Driver.py -v -mode solver in2.txt
```


## Note:
- The permissible values of mode are:
  - `cnf` (In mode "cnf" you should expect a BNF input file, convert to CNF and print to console),
  - `dpll` (In mode "dpll" you should expect a CNF input file, which you solve using the DPLL algorithm printing the solution to console),
  - `solver` (In mode "solver" you should expect a BNF input file, run cnf mode, but instead of printing, send the input to dpll mode)
