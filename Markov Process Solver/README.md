## Objective

Implement a generic Markov Process Solver using value iteration and greedy policy computation.

The program should take 4 flags (which will be understood better later) and an input file.

-df : a float discount factor [0, 1] to use on future rewards, defaults to 1.0 if not set
-min : minimize values as costs, defaults to false which maximizes values as rewards
-tol : a float tolerance for exiting value iteration, defaults to 0.01
-iter : an integer that indicates a cutoff for value iteration, defaults to 100


**Value Iteration** computes a transition matrix using a fixed policy, then iterates by recomputing values for each node using the previous values until either:
1. no value changes by more than the 'tol' flag, or 
2. -iter iterations have taken place.

**Greedy Policy Computation** uses the current set of values to compute a new policy. If -min is not set, the policy is chosen to maximize rewards; if -min is set, the policy is chosen to minimize costs.

The value of an individual state is computed using the Bellman equation for a Markov property
`v(s) = r(s) + df * P * v`
Where:
v on the RHS is the previous values for each state
df is the -df discount factor flag applied to future rewards
P is the transition probability matrix computed using the policy and the type of node this is 
r(s) is the reward/cost for being in this particular state.

## Running the program

Requirement: Python 3

Library used: numpy

```
usage: mdp.py [-min] -df $df -tol $tol -iter $iter $filename

positional arguments:
  filename              specify the input file to be read

optional arguments:
  -h, --help            show this help message and exit
  -min, --min           minimize values as costs, defaults to false (if not set) which maximizes values as rewards.
  -tol TOL, --tol TOL   a float tolerance for exiting value iteration, defaults to 0.01
  -iter ITER, --iter ITER
                        an integer that indicates a cutoff for value iteration, defaults to 100
  -df DF, --df DF       a float discount factor [0, 1] to use on future rewards, defaults to 1.0 if not set
```

Examples:

```
python3 mdp.py -df 1.0 -tol 0.001 -iter 100 in1.txt
python3 mdp.py -df 0.9 -tol 0.001 -iter 100 -min in3.txt

```


## Note:
- The permissible values of df should be in [0, 1], Default value is 1.0.
- Default value of tolerance is 0.01 if not set.
- Default value for iter is 100 if not set.