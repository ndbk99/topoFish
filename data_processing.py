import csv
import math
import matplotlib.pyplot as plt
from scipy import cluster
import time as t
from math import radians, cos, sin, asin, sqrt

"""
open and read data from file
input: file name
output: list of observation objects created from file dat
"""
def read_data(f):
	data = []
	with open(f, "r") as csvfile:
		r = csv.reader(csvfile, delimiter=",")
		for row in r:
			x = observation(row[0], row[2], row[7], row[8], int(row[12]))
			data.append(x)
	return data

"""
class to hold observation datum
parameters: index, species, longitude, latitude, timestamp
"""
class observation(object):

	def __init__(self, index, species, longitude, latitude, time):
		self.index = int(index)
		self.species = species
		self.longitude = float(longitude)
		self.latitude = float(latitude)
		self.time = time

	def toString(self):
		print(self.index, self.species, self.latitude, self.longitude)

"""
create subset of observations that are of given species at given time
input: data to take subset of, name of species, time
output: set of observations that match the input parameters
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
calculate the great circle distance between two points on the earth (specified in decimal degrees)
input: longitude and latitude of first point, longitude and latitude of second point
output: distance in km between the two points on the earth's surface
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
create condensed distance matrix
input: data set of latitutes, longitudes for 1 species in 1 year
output: array containing flattened upper triangular matrix of distances between observations in km calculated using haversine formula
*** USED FOR CLUSTERING
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
create full distance matrix
input: data set of latitutes, longitudes for 1 species in 1 year
output: array containing matrix of distances between observations in km calculated using haversine formula
*** USED FOR DISPLAY ONLY
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
find the cluster distribution for a data set
input: set of observations of 1 species in 1 year
output: some kind of data structure of clusters ?
"""
def clusters(data):
	matrix = cond_matrix(data)
	if len(data) > 1:
		clusters = cluster.hierarchy.single(matrix)
		cut = cluster.hierarchy.cut_tree(clusters, n_clusters=None, height=100)
		return cut
		# NOT WORKING :((( idk why ?????
	else:
		return 0

############# PLOTTING #########################################################

"""
plot one data set (all observations of one species at one time)
input: set of observations of 1 species at 1 time
output: plot of data points
"""
def plot_set(data):
	plt.scatter([x.longitude for x in data], [x.latitude for x in data])
	plt.axis([-175.5,-157.5,49.5,66.0])
	# plt.axis([min_long - 1, max_long + 1, min_lat - 1, max_lat + 1])
	plt.show()

"""
plot clusters of data
input: set of observations of 1 species at 1 time, clustering parameter (default = 1.0)
output: plot of data points colored by cluster
"""
def plot_clusters(data):

	# can't perform clustering on 0 or 1 points so exit function
	if len(data) < 2:
		plt.show()
		return 0

	clustering = clusters(data)

	plt.axis([-175.5,-157.5,49.5,66.0])
	# plt.axis([min_long - 1, max_long + 1, min_lat - 1, max_lat + 1])

	for i in range(len(data)):

		cluster = clustering[i]

		if cluster % 4 == 0:
			c = "red"
		elif cluster % 4 == 1:
			c = "blue"
		elif cluster % 4 == 2:
			c = "green"
		elif cluster % 4 == 3:
			c = "black"

		plt.scatter(data[i].longitude, data[i].latitude, color=c)

	plt.show()
	plt.close()

"""
create animation of observations of a certain species over the years
input: set of observations of 1 species over all years
output: animated plot of the species over the years
"""
def animate(data, species):

	# plt.ion()  # set plotting mode to interactive or whatever
	plt.show()

	print(species)

	# animate data from time to time
	i = 1
	for time in range(1984,2015):

		time_subset = data_subset(data,species,time)

		# plot current figure
		fig = plt.figure(i)
		plt.scatter([x.longitude for x in time_subset], [x.latitude for x in time_subset])
		plt.axis([-175.5,-157.5,49.5,66.0]) # CHANGE AXIS BOUNDARIES TO LIMITS OF RYAN'S GIF
		# plt.axis([min([x.longitude for x in data]) - 1, max([x.longitude for x in data]) + 1, min([x.latitude for x in data]) - 1, max([x.latitude for x in data]) + 1])

		# draw and then clear current points
		plt.draw()
		plt.pause(0.00005)
		plt.clf()

	plt.close()


################################################################################
################################################################################

clustered_species = ['Aforia circinata','Argis dentata', 'Argis lar', 'Artediellus pacificus', 'Buccinum polare', 'Ciliatocardium ciliatum', 'Crangon dalli', 'Cyanea capillata', 'Echinarachnius parma', 'Elegius gracilis', 'Eunoe depressa', 'Euspira pallida', 'Gersemia rubiformis', 'Glebocarcinus oregonensis', 'Grandicrepidula grandis', 'Halichondria panicea', 'Halocynthia aurantium', 'Hiatella arctica', 'Icelus spatula', 'Icelus spiniger', \
'Leptasterias groenlandica', 'Limanda sakhalinensis', 'Liparis gibbus', 'Lycodes raridens', 'Mactromeris polynyma', 'Matridium farcimen', 'Musculus discors', 'Neocrangon communis', 'Ophiura sarsii', 'Pyrulofusus melonis', 'Rhamphostomella costata', 'Serratiflustra serrulata', 'Siliqua alta', 'Stomphia coccinea', 'Tellina lutea', 'Trichodon trichodon', 'Triglops pingelii', 'Triglops scepticus', 'Tritonia diomedea', 'Urticina crassicornis', 'Volutopsius fragilis', 'Volutopsius middendorffii']

## CURRENT MAIN
data = read_data("mydata.csv")  # list of observation objects
subset = data_subset(data,"Aforia circinata",1987)  # observations of Aforia circinata in 1987
upper = cond_matrix(subset)  # condensed distance matrix ?? FIX THIS
cluster_set = clusters(subset)  # clustering structure of data subset

# mins and maxes for plotting
min_long = min([x.longitude for x in data])
min_lat = min([x.latitude for x in data])
max_long = max([x.longitude for x in data])
max_lat = max([x.latitude for x in data])

# print distance matrix
for row in dist_matrix(subset):
	print(row)
print(len(dist_matrix(subset)))

# print clustering alongside corresponding points
for i in range(len(subset)):
	print("cluster", cluster_set[i][0], "(", subset[i].longitude, ",", subset[i].latitude, ")")

clusterset_array = []
for x in cluster_set:
	clusterset_array.append(x[0])

# plot the subset
plot_clusters(subset)
