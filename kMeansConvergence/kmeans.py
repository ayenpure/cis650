import sys
import os
import math
from multiprocessing import Pool,current_process,cpu_count,active_children
from timeit import default_timer as timer
from functools import partial

# Parameter for number of cores to use
useCores = 4

def start_process():
    #print( 'Starting {} with pid {}'.format(current_process().name,current_process().pid)) 
    #delayed print from when pool initialized
    return

#
# Phase 1 functions
#

def readBoyanaFile(fname):
    fid = open(fname,'r')
    data = fid.readlines()
    l = map(lambda line : map(float, line.rstrip().split())[:-1],data)
    return {i:v for i,v in enumerate(l)}

def readElectricFile(fname):
    fid = open(fname,'r')
    data = filter(lambda x : "?" not in x, fid.readlines()[1:])
    l = map(lambda line : map(float, (line.rstrip().split(';'))[2:]),data)
    return {i:v for i,v in enumerate(l)}

# Function to calculate euclidean distance
def euclidean_distance(vec1, vec2):
    zipped = zip(vec1, vec2)
    sqdiff = map(lambda pair: (pair[0] - pair[1])**2, zipped)
    summation = sum(sqdiff)
    return math.sqrt(summation)

# Function to associate a point with a cluster
def compute_center(point, all_centers):
    value = point[1]
    centers_list = all_centers.items()
    distances = map(lambda pair: (pair[0], euclidean_distance(value, pair[1])), centers_list)
    tup = min(distances, key=lambda t: t[1])
    return tup[0]

#
# Phase 2 functions
#

# Function to calculate the centroid given the clusterId and all points.
def getCentroid(clusterId, clusters):
    cluster = map(lambda pair : pair[1] ,filter(lambda pair : pair[0] == clusterId , clusters))
    compactCluster = zip(*cluster)
    centroid =  [sum(component) / len(component) for component in compactCluster]
    return centroid

# Function to recalculate centers given clusterIds, the cluster mappings
# and the all the points.
def recalculateCenters(pool, clusterIds, mapping, items):
    clusters = zip(mapping, items)
    partialGetCentroids = partial(getCentroid, clusters = clusters)
    centroids = map(partialGetCentroids, clusterIds)
    return {key:value for key,value in zip(clusterIds,centroids)}

def compareCenters(centersPair):
    for pair in zip(centersPair[0], centersPair[1]):
        if(pair[0] != pair[1]):
            return 1
    return 0

def main():
    readFile = 0;
    numClusters = 3; 
    numargs = len(sys.argv)
    if(numargs == 3):
       readFile = sys.argv[1]
       numClusters = sys.argv[2]
    elif(numargs == 2):
       readFile = sys.argv[1]

    print readFile

    batch = {}
    myDir = os.path.expanduser("./")
    if(readFile == 0):
        myFile = "N_combinedLogs_hourly.txt"
        batch = readBoyanaFile(myDir + myFile)
    else:
        myFile = "household_power_consumption.txt"
        batch = readElectricFile(myDir + myFile)

    print('Total points: ' + str(len(batch)) )  # 4338
    print('First line: {}'.format(batch.items()[0]))

    batchLength = len(batch)
    initCenters = {1: batch[batchLength/2], 2: batch[batchLength/3], 3: batch[batchLength/5]}  # keep this to reset to
    centers = initCenters
    print('Intital Centers : \n')
    print centers

    # Create pool for the entire program
    processors = cpu_count()
    print("Total cores available: {}".format(processors)) 
    print("Total cores used: {}".format(useCores))
    pool = Pool(processes=useCores, initializer=start_process)
   
    iterations = 50
    print("Maximum number of iterations: {}".format(iterations))
    total_time = 0
    centerIds = centers.keys()
    items = batch.values()
    for i in range(iterations):
        print("Starting iteration " + str(i))
        start = timer()
        #moved this inside loop b/c gets updated after each iteration
        partialCompute = partial(compute_center, all_centers = centers) 
        new_p_to_c_map = pool.map(partialCompute, batch.items())
        end = timer()
        t = end - start
        total_time += t
        print( "Time of part 1: " + str(t))
        start = timer()
        #compute new values of centers
        newCenters = recalculateCenters(pool, centerIds, new_p_to_c_map, items)
        end = timer()
        t = end - start
        total_time += t
        print( "Time of part 2: " + str(t))

        changedCenters = 0;
        for tup in zip(centers.values(), newCenters.values()):
            changedCenters += compareCenters(tup);

        centers = newCenters  # update centers with new values
        if changedCenters == 0:
            break  # last iteration caused no allegiance changes
    
    pool.close() # no more tasks
    pool.join()  # wrap up current tasks
    print("Total time: " + str(total_time))

if __name__ == "__main__":
    main()
