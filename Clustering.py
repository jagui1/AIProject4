# Jeremy Aguillon
# CMSC 471
# Project 4 - K Means implementation
# Usage: python3 Clustering.py numberOfClusters file.txt

# matplotlib imports
#%matplotlib inline
import matplotlib.pyplot as plt
import matplotlib.colors as colors
# random import for initial clusters
from numpy.random import randint
# math for finding distance between points
from math import hypot
# imports sys for command line arguments (argv)
import sys

## Constants ##
INPUT = 2
CLUSTERS = 1

# getData takes in data from a given file in the form <xcoord> <ycoord> \n
# Input: filename - string of the file to open
# Output: points - a list of tuples that represent data points
def getData(filename):
    # opens and closes file
    with open(filename, 'r') as myFile:
        # initalizes point list
        points = []

        # gets data
        for line in myFile:
            line = line.strip().split()
            points.append( ( float(line[0]), float(line[1]) ) )

    return points  


# getRndClusters() gets the initial random clusters that represent the first means
# Input: numClusters - number of clusters being used 
#        points - list of all points
# Output: clusters - a list of tuples representing the starting k means
def getRndClusters(numClusters, points):
    # initialize clusters
    clusters = []
    
    # gets the correct amount of clusters
    for i in range(numClusters):
        curPoint = -1
        # keeps looping until it finds a unique cluster
        while len(clusters) == i:
            # randomly selects clusters until a new one is found
            curPoint = points[randint(0, len(points))]
            if curPoint not in clusters:
                clusters.append(curPoint)

    return clusters


# getNewClusters() after each iteration of the loop the mean of each of the groups
#                  are set to the new group of k clusters
# Input: clusterDict - a dictionary mapping each mean to the points associated with it
# Output: clusters - the new means of each group
#         clusterDict - dictionary of previous iteration to count how many changed
def getNewClusters(clusterDict):
    # initialize counters
    counter = 0
    xSum = 0
    ySum = 0
    clusters = []

    # loops through each group to calculate
    for key in clusterDict.keys():
        # adds key value
        counter = 1
        xSum = key[0]
        ySum = key[1]

        # adds key group values
        for point in clusterDict[key]:
            counter += 1
            xSum += point[0]
            ySum += point[1]

        # gets the mean
        curClus = ( xSum/counter, ySum/counter )

        # ensures there is a unique cluster added
        if curClus not in clusters:
            clusters.append( curClus )
        elif key not in clusters:
            clusters.append( key )
        else:
            for miniPoint in clusterDict[key]:
                if miniPoint not in clusters:
                    clusters.append(miniPoint)
                    break

    return clusters, clusterDict   
    

# plotFinal() plots the final groupings and means using pyplot
# Input: clusterDict - a dictionary mapping each mean to the points associated with it
#        points - the list of all points to find the axis
# Output: None
def plotFinal(clusterDict, points):
    # colors to identify each group
    colors = ['ko','bo', 'go', 'ro',  'mo', 'yo', 'co', 'wo']
    clstColors = ['k^','b^', 'g^', 'r^',  'm^', 'y^','c^',  'w^']
    # color count changes for each key (group)
    colorCount = 0

    # loops through each group
    for key in clusterDict.keys():
        # sets the color for the points
        curColor = colors[( colorCount%len(colors) )]
        # sets the color for the mean
        curClstColor = clstColors[( colorCount%len(colors) )]
        # plots
        plt.plot(key[0], key[1], curClstColor, label="cluster "+str(colorCount+1))
        plt.plot( [x[0] for x in clusterDict[key]], [y[1] for y in clusterDict[key]], curColor, label="points "+str(colorCount+1))
        # sets the axis so you can see all points
        axis = [min([x[0] for x in points])-1, max([x[0] for x in points])+1, min([y[1] for y in points])-1, max([y[1] for y in points])+1]
        plt.axis(axis)
        # increments color count
        colorCount += 1

    # creates a legend across the top
    plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=2, mode="expand", borderaxespad=0.)
    # shows the plot
    plt.show()


# kMeans() performs k means clustering on the given data points 
#          with numClusters amount of means
# Input: numClusters - number (k) of means that will be used
#        points - list of all data points being clustered
# Output: None
def kMeans(numClusters, points):
    # initializes the k clusters
    clusters = getRndClusters(numClusters, points)
    # dict that represents the previous iteration of clusters
    old = {}
    # initializes changed points so it goes into the loop
    changed = 100

    # loops until no points change clusters
    while changed > 0:
        # counter for changed points
        changed = 0
        # resets cluster dictionary to a dictionary with 1 key per k cluster
        clusterDict = {}

        for cluster in clusters:
            clusterDict[cluster] = []

        # loops through each point
        for point in points:
            # does not perform calculations on clusters
            if point not in clusters:
                # finds the closest cluster distance wise
                Min = float('inf')
                minClus = -1
                for cluster in clusters:
                    curMin = hypot( cluster[0] - point[0], cluster[1] - point[1] )
                    if curMin < Min:
                        Min = curMin
                        minClus = cluster
                
                # changes the point to the closest cluster
                if minClus != 1:
                    clusterDict[minClus].append(point)

                    # checks if the point changed or not and updates counter
                    if minClus in old.keys():
                        if point not in old[minClus]:
                            changed += 1
                    else: 
                        changed += 1
                # something went wrong if this prints, not sure how it would though
                else:
                    print("Error min not found")

        # updates the clusters for each iteration
        clusters, old = getNewClusters(clusterDict)

    # plots the final groupings
    plotFinal(clusterDict, points)

# main function
def main(argv):
    # input validation
    if len(argv) != 3:
        print("Invalid input!\nUsage: python Clustering.py <numberOfClusters> <input file>")
    else:
        # does the clustering
        points = getData(argv[INPUT])
        kMeans(int(argv[CLUSTERS]), points)
        

# call to main
#main(["clustering.py", "4", "input.txt"])
main(sys.argv)
