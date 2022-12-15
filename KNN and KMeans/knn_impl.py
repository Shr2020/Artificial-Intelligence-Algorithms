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

def form_data_dict(train_data):
    train_dict = dict()
    for ind, x in enumerate(train_data):
        train_dict[ind] = x[-1]
    return train_dict

def get_classes(train_data):
    classes = set()
    for row in train_data:
        classes.add(row[-1])
    return classes

def get_knearest_neighbors(test_point, train_data, use_e2, k):
    dist = list()

    for train_point in train_data:
        distance = calc([float(train_point[i]) for i in range(len(train_point)-1)], test_point, use_e2)
        dist.append((distance, train_point[-1]))

    dist.sort(key=lambda x: x[0])
    knearest = [dist[i] for i in range(k)]
    return knearest

def make_pred(point_num, knearest, actual, use_wt):
    if not use_wt:
        exp_clus = [x[1] for x in knearest]
        actual_cluster = max(exp_clus, key=exp_clus.count)
        actual[point_num] = actual_cluster
    else:
        clust_wt = dict()
        for x in knearest:
            if x[-1] in clust_wt:
                d = max(x[0], 0.0001)
                clust_wt[x[-1]]+=1/d
            else:
                d = max(x[0], 0.0001)
                clust_wt[x[-1]] = 1/d
        actual_cluster = max(clust_wt, key=clust_wt.get)
        actual[point_num] = actual_cluster
    return actual_cluster


def make_all_predictions(test_data, train_data, test_dict, method, wt, k):
    actual = dict()
    point_num = 0
    for row in test_data:
        test_pnt = [float(row[i]) for i in range(len(row)-1)]
        knearest = get_knearest_neighbors(test_pnt, train_data, method, k)
        act = make_pred(point_num, knearest, actual, wt)
        point_num += 1
        print("Wanted:", row[-1], "Got:", act)

    return actual

def calculate_precision_recall(expected, actual, classes, length):
    true_pos = {}
    relevent = {}
    identified = {}
    class_list = list(classes)
    class_list.sort()
    for cl in class_list:
        true_pos[cl] = 0
        relevent[cl] = 0
        identified[cl] = 0
    for i in range(length):
        if expected[i] == actual[i]:
            true_pos[actual[i]] += 1
        identified[actual[i]] += 1
        relevent[expected[i]] +=1
    
    for cl in class_list:
        precision = str(true_pos[cl]) + "/" + str(identified[cl])
        recall = str(true_pos[cl]) + "/" + str(relevent[cl])
        print("Label:", cl, "Precision:", precision, "Recall:", recall)
    


def driver(train_file, test_file, k, use_e2, unitw):
    use_wt = not unitw
    train_data = read_csv(train_file)
    test_data = read_csv(test_file)
    expected = form_data_dict(test_data)
    length = len(test_data)
    classes = get_classes(train_data)
    actual = make_all_predictions(test_data, train_data, expected, use_e2, use_wt, k)
    calculate_precision_recall(expected, actual, classes, length)

    






