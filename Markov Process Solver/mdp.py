import Helper
import argparse
import sys
import Markov

df = 1.0
iter = 100
tol = 0.01
min=False
fname = ""
arguments_valid = True

parser = argparse.ArgumentParser()
parser.add_argument("-min", "--min", help="minimize values as costs, defaults to false (if not set) which maximizes values as rewards.", action="store_true")
parser.add_argument("-tol", "--tol", help="a float tolerance for exiting value iteration, defaults to 0.01", type=float, default=0.01)
parser.add_argument("-iter", "--iter",  help="an integer that indicates a cutoff for value iteration, defaults to 100", type=int, default=100)
parser.add_argument("-df", "--df", help="a float discount factor [0, 1] to use on future rewards, defaults to 1.0 if not set", type=float, default=1.0)
parser.add_argument("filename", help="specify the input file to be read")
args = parser.parse_args()

fname = args.filename

if args.df:
    df = args.df

if args.iter:
    iter = args.iter
    
if args.tol:
    tol = args.tol

if args.min:
    min = True

result = ""
nodes_list = []
node_dict = {}
decision_node_dict = {}
chance_node_dict = {}
reward_dict = {}

try:
    nodes_list, node_dict, decision_node_dict, chance_node_dict, reward_dict = Helper.read_file(fname)
except FileNotFoundError as e:
    print("Error Opening File:" + str(e))
    arguments_valid = False

if df < 0.0 or df > 1.0:
    print("Invalid input argument discount factor (-df) value. Value of discount factor should be within [0,1]")
    arguments_valid = False

if iter <= 0:
    print("Invalid input argument iteration (-iter) value. Value of iterations should be positive value.")
    arguments_valid = False

if arguments_valid:
    arguments_valid = Helper.check_nodes(nodes_list)

if arguments_valid:
    arguments_valid = Helper.check_terminal_nodes(node_dict, nodes_list, decision_node_dict, chance_node_dict)

if arguments_valid:
    Markov.driver(nodes_list, node_dict, decision_node_dict, chance_node_dict, reward_dict, iter, df, tol, min)
    True

if not arguments_valid:
    print("Invalid file/arguments.")
    sys.exit(1)