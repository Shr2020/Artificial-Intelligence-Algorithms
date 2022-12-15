import argparse
import sys
import knn_impl


train_fname = ""
test_fname = ""
unitw = False
arguments_valid = True
k = 3
use_e2 = False

parser = argparse.ArgumentParser()
parser.add_argument("-k", "--k", help="k nearest neighbors", type=int, default=3)
parser.add_argument("-unitw", "--unitw", help="whether to use unit voting weights. If not set then use (1/d)", action="store_true")
parser.add_argument("-d", "--d",  help="specify the mode of distance calculation. Permissible value = e2/manh", required=True)
parser.add_argument("train_file", help="specify the training file to be read")
parser.add_argument("test_file", help="specify the test file to be read")
args = parser.parse_args()

train_fname = args.train_file
test_fname = args.test_file

if args.unitw:
    unitw = args.unitw

if args.k:
    k = args.k
    
if args.d == "e2":
    use_e2 = True
elif args.d == "manh":
    use_e2 = False
elif args.d != "e2" or args.d != "manh":
    arguments_valid = False

if arguments_valid:
    knn_impl.driver(train_fname, test_fname, k, use_e2, unitw)

if not arguments_valid:
    print("Invalid file/arguments.")
    sys.exit(1)