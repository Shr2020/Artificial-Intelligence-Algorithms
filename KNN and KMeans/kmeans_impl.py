from csv import reader
from math import sqrt

def calc(p1, p2, euc):
    if len(p1) == 3:
        if euc:
            return ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2 + (p1[2] - p2[2])**2)
        else:
            return (abs(p1[0] - p2[0]) + abs(p1[1] - p2[1]) + abs(p1[2] - p2[2]))
    else:
        if euc:
            return ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)
        else:
            return (abs(p1[0] - p2[0]) + abs(p1[1] - p2[1]))

# Load a CSV file
def read_csv(filename):
	train_data = list()
	with open(filename, 'r') as file:
		csv_reader = reader(file)
		for row in csv_reader:
			if not row:
				continue
			train_data.append(row)
	return train_data

def form_train_data_dict(data):
    data_dict = dict()
    for x in data:
        data_dict[x[-1]] = [float(x[i]) for i in range(len(x)-1)]
    return data_dict

def form_data_dict(data):
    data_dict = dict()
    for ind, x in enumerate(data):
        data_dict[ind] = x[-1]
    return data_dict

def create_inititial_centroids_dict(initial_centroids):
    centroids = {}
    cluster_num = 1
    for cent in initial_centroids:
        name = "C"+str(cluster_num)
        centroids[name] = list(cent)
        cluster_num+=1
    return centroids

def calculate_new_centroids(cluster_dict, train_data_dict, existing_cent):
    centroids = {}
    for cluster in cluster_dict:
        mean = list()
        points = cluster_dict[cluster]
        for p in points:
            pnt = train_data_dict[p]
            for i, x in enumerate(pnt):
                if i+1 > len(mean):
                    mean.append(x)
                else:
                    mean[i]+=x
        length = len(points)
        if length == 0:
            centroids[cluster] = existing_cent[cluster]
        else:
            centroids[cluster] = [x/float(length) for x in mean]    
    return centroids


def create_cluster_set(centroids):
    clusters = {}
    for cluster_name in centroids:
        clusters[cluster_name] = set()
    return clusters

def form_clusters(train_data, cents, euc, train_data_dict):
    stay = True
    centroids = cents.copy()
    clusters = create_cluster_set(centroids)
    while(stay):
        new_clusters = create_cluster_set(centroids)
        for train_row in train_data:
            minD = float('inf')
            centr = ""
            for cent in centroids:
                p1 = centroids[cent]
                dist = calc([float(train_row[i]) for i in range(len(train_row)-1)], p1, euc)
                if dist < minD:
                    minD = dist
                    centr = cent
            new_clusters[centr].add(train_row[-1])
        if (clusters == new_clusters):
            stay = False
            for c in new_clusters:
                print(c, ":", new_clusters[c], '\n')
            print(centroids)
        else:
            new_centroids = calculate_new_centroids(new_clusters, train_data_dict, centroids)
            centroids = new_centroids.copy()
            clusters = new_clusters.copy()



def driver(filename, use_euc, initial_centroids):
    train_data = read_csv(filename)
    train_data_dict = form_train_data_dict(train_data)
    centroids = create_inititial_centroids_dict(initial_centroids)
    form_clusters(train_data, centroids, use_euc, train_data_dict)

