import argparse
import sys
import kmeans_impl

use_e2 = False
arguments_valid = True

parser = argparse.ArgumentParser()
parser.add_argument("-data", "--data",  help="file containing data", required=True)
parser.add_argument("-d", "--d",  help="specify the mode of distance calculation. Permissible value = e2/manh", required=True)
parser.add_argument("centroids",nargs="+", help="specify the centroids")
args = parser.parse_args()

fname = args.data
centroids = args.centroids
if args.d == "e2":
    use_e2 = True
elif args.d == "manh":
    use_e2 = False
elif args.d != "e2" or args.d != "manh":
    arguments_valid = False

def convert_centroids(centroids):
    cent = []
    for c in centroids:
        x_arr = c.split(',')
        x = [s.strip() for s in x_arr] 
        if len(x) > 2 :
            cent.append([float(x[0]), float(x[1]), float(x[2])])
        else:
            cent.append([float(x[0]), float(x[1])])
    return cent

initial_centroids = convert_centroids(centroids)

if arguments_valid:
    kmeans_impl.driver(fname, use_e2, initial_centroids)

if not arguments_valid:
    print("Invalid file/arguments.")
    sys.exit(1)