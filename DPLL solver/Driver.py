import argparse
import sys
import Helper
import CNFToDPLL
import BNFToCNF
import DPLLSolver

verbose = False
mode = ""
fname = ""

parser = argparse.ArgumentParser()

parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
parser.add_argument("-mode", "--mode", help="specify the mode. Permissible value = cnf, dpll, solver", required=True)
parser.add_argument("filename", help="specify the input file to be read")
args = parser.parse_args()

fname = args.filename
if args.verbose:
    verbose = True
mode = args.mode
arguments_valid = True
text_valid = True
result = []

try:
    result = Helper.read_file(fname)
except FileNotFoundError as e:
    print("Error Opening File:" + str(e))
    arguments_valid = False


if arguments_valid:
    if not Helper.is_mode_valid(mode.lower()):
        print("Algorithm (-algo) not valid. The permissible values are bfs, id or a_star.")
        arguments_valid = False

if arguments_valid:
    if mode.lower() == "cnf" or mode.lower() == "solver":
        if not Helper.is_bnf_text_valid(result):
            print("Invalid input file contents.")
            text_valid = False
            sys.exit(1)
    if mode.lower() == "dpll":
        if not Helper.is_cnf_text_valid(result):
            print("Invalid input file contents.")
            text_valid = False
            sys.exit(1)
    


if arguments_valid:
    if mode.lower() == "cnf":
        BNFToCNF.bnf_to_cnf(result)
    elif mode.lower() == "dpll":
        CNFToDPLL.dpll(verbose, result)
    elif mode.lower() == "solver":
        DPLLSolver.solver(verbose, result)
        

if not arguments_valid:
    sys.exit(1)

if not text_valid:
    sys.exit(1)
