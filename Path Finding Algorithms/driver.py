import Helper
import BFS
import ID
import A_star
import argparse
import Graph
import sys

verbose = False
start = ""
goal = ""
algo = ""
fname = ""
depth = 0
arguments_valid = True

parser = argparse.ArgumentParser()

parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
parser.add_argument("-start", "--start", help="specify the starting node", required=True)
parser.add_argument("-end", "--end",  help="specify the ending node", required=True)
parser.add_argument("-algo", "--algo", help="specify the algorithm to use. Permissible values = BFS, ID, A_star", required=True)
parser.add_argument("filename", help="specify the input file to be read")
parser.add_argument("-depth", "--depth", help="depth for iterative deepening", type=int, default=2)
args = parser.parse_args()

fname = args.filename
if args.verbose:
    verbose = True
start = args.start
end = args.end
algo = args.algo
depth = args.depth
result = ""
node_dict = {}
edges = []

try:
    result = Helper.read_file(fname)
except FileNotFoundError as e:
    print("Error Opening File:" + str(e))
    arguments_valid = False

if arguments_valid:
    node_dict = result[0]
    edges = result[1]
    if not Helper.check_edge_valid(node_dict, edges):
        print("Check the input file. The graph is not valid. The edges does not belong to nodes of the graph.")
        arguments_valid = False

    if not Helper.is_node_valid(node_dict, start):
        print("start node (-start) not in the graph")
        arguments_valid = False

    if not Helper.is_node_valid(node_dict, end):
        print("end node (-end) not in the graph")
        arguments_valid = False

    if not Helper.is_algo_valid(algo.lower()):
        print("Algorithm (-algo) not valid. The permissible values are bfs, id or a_star.")
        arguments_valid = False

if arguments_valid:
    # create graph 
    graph = Graph.Graph()
    graph.add_edges(node_dict, edges)
    graph.sort_edges()
    if algo.lower() == "bfs":
        BFS.breadth_first_search(graph, start, end, verbose)
    elif algo.lower() == "id":
        ID.iterative_deepening(graph, start, end, depth, verbose)
    elif algo.lower() == "a_star":
        A_star.A_star(graph, node_dict, start, end, verbose)

if not arguments_valid:
    sys.exit(1)