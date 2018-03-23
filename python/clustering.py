import csv
from scipy.cluster import *
from math import radians, cos, sin, asin, sqrt


############# SETUP ############################################################

"""
Open and read data from file
Input: file name
Output: list of observation objects created from file dat
"""
def read_data(f):
	data = []
	with open(f, "r") as csvfile:
		r = csv.reader(csvfile, delimiter=",")
		for row in r:
			x = observation(row[0], row[2], row[7], row[8], row[12])
			data.append(x)
	return data

"""
Class to hold observation datum
Parameters: index, species, longitude, latitude, timestamp
"""
class observation(object):

	def __init__(self, index, species, longitude, latitude, time):
		self.index = int(index)
		self.species = species
		self.longitude = float(longitude)
		self.latitude = float(latitude)
		self.time = int(time)

	def toString(self):
		print(self.index, self.species, self.latitude, self.longitude)

"""
Create subset of observations that are of given species at given time
Input: data to take subset of, name of species, time
Output: set of observations that match the input parameters
"""
def data_subset(data,species,time):

	result = []

	if time == "none":
		for x in data:
			if x.species == species:
				result.append(x)
	elif species == "none":
		for x in data:
			if x.time == time:
				result.append(x)
	else:
		for x in data:
			if x.species == species and x.time == time:
				result.append(x)

	return result


############# CLUSTERING #######################################################

"""
Calculate the great circle distance between two points on the earth (specified in decimal degrees)
Input: longitude and latitude of first point, longitude and latitude of second point
Output: distance in km between the two points on the earth's surface
source - https://stackoverflow.com/questions/4913349/haversine-formula-in-python-bearing-and-distance-between-two-gps-points#comment5473498_4913653
"""
def haversine(lon1, lat1, lon2, lat2):
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r

"""
Create condensed distance matrix
Input: data set of latitutes, longitudes for 1 species in 1 year
Output: array containing flattened upper triangular matrix of distances between observations in km calculated using haversine formula
USED FOR CLUSTERING CALCULATIONS
"""
def cond_matrix(data):
	cond = []
	for x in range(len(data)):
		for y in range(len(data)):
			if (y > x):  # *** only calculate distances for point pairs in upper (right!) triangular MINUS diagonal! this is the form of the condensed distance matrix ***
				dist = haversine(data[x].longitude, data[x].latitude, data[y].longitude, data[y].latitude)  # calculate distance between points using Haversine formula
				cond.append(dist)  # append distance to condensed matrix
	return cond

"""
Create full distance matrix
Input: data set of latitutes, longitudes for 1 species in 1 year
Output: array containing matrix of distances between observations in km calculated using haversine formula
USED FOR DISPLAY ONLY
"""
def dist_matrix(data):
	matrix = []
	for x in range(len(data)):
		row = []
		for y in range(len(data)):
			if (y > x):  # see note in cond_matrix
				dist = haversine(data[x].longitude, data[x].latitude, data[y].longitude, data[y].latitude)  # calculate distance between points using Haversine formula
				row.append(round(dist,1))  # append distance to condensed matrix
			else:
				row.append(0.0)
		matrix.append(row)
	return matrix

"""
Find the cluster distribution for a data set
Input: set of observations of 1 species in 1 year
Output: list of cluster identification indices
"""
def clusters(data):

	matrix = cond_matrix(data)

	if len(data) > 1:
		clusters = cluster.hierarchy.single(matrix)  # Use single hclust method to create linkage matrix clustering dendrogram structure thing
		cut_param = 150  # Parameter suggested by Ryan is 100, but test out several
		cut = cluster.hierarchy.cut_tree(clusters, n_clusters=None, height=cut_param)  # Cut linkage matrix
		result = [x[0] for x in cut]
		return result

	elif len(data) == 1:
		return [0]

	else:
		return 0
