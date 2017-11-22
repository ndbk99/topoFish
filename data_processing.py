import csv
import math
from graphics import *
import matplotlib.pyplot as plt
from scipy.cluster import hierarchy

"""
class to hold observation datum
parameters: index, species, longitude, latitude, time
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
create subset of observations that are of given species at given time
input: data to take subset of, name of species, time
"""
def data_subset(data,species,time):

	result = []

	if species == "none":
		for x in data:
			if x.time == time:
				result.append(x)
	elif time == "none":
		for x in data:
			if x.species == species:
				result.append(x)
	else:
		for x in data:
			if x.species == species and x.time == time:
				result.append(x)

	return result

"""
plot one data set (all observations of one species at one time)
input: set of observations of 1 species at 1 time
output: plot of data points
"""
def plot_set(data):
	plt.scatter([x.longitude for x in data], [x.latitude for x in data])
	plt.axis([min_long - 1, max_long + 1, min_lat - 1, max_lat + 1])
	plt.show()

"""
plot clusters of data
input: set of observations of 1 species at 1 time, clustering parameter (default = 1.0)
output: plot of data points colored by cluster
"""
def plot_clusters(data,param=1.0):

	# can't perform clustering on 0 or 1 points so exit function
	if len(data) < 2:
		plt.show()
		return 0

	clustering = clusters(data,param)

	plt.axis([min_long - 1, max_long + 1, min_lat - 1, max_lat + 1])

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
create animation of observations of a certain species over the times
input: set of observations of 1 species over all times
output: animated plot of the species over the times
"""
def animate(data):

	# plt.ion()  # set plotting mode to interactive or whatever
	plt.show()

	# animate data from time to time
	i = 1
	for time in range(1984,2015):

		print(time)
		time_subset = data_subset(data,species,time)

		# plot current figure
		fig = plt.figure(i)
		plt.scatter([x.longitude for x in time_subset], [x.latitude for x in time_subset])
		plt.axis([min_long - 1, max_long + 1, min_lat - 1, max_lat + 1])

		# draw and then clear current points
		plt.draw()
		plt.pause(0.05)
		plt.clf()

"""
find the cluster distribution for a data set
input: set of observations of 1 species in 1 year, clustering parameter
output: list of cluster indices for the observations
"""
def clusters(data,param=1):
	points = [[x.longitude, x.latitude] for x in data]
	if len(points) > 1:
		clusters = hierarchy.fclusterdata(points,param)
		return clusters
	else:
		return 0

"""
modified range function to allow floats - used to test out different param values in fclusterdata
input: floats to set start and stop values, step between values
output: list of floats from start to stop, separated by step
"""
def frange(start, stop, step):
	result = []
	i = start
	while i < stop:
		yield i
		i += step
		result.append(i)
	return result

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
			x = observation(row[0], row[2], row[7], row[8], row[12])
			data.append(x)
	return data

###############################################################################

data = read_data("mydata.csv")

# create subset of data
species = 'Trichodon trichodon'#'Platichthys stellatus' # 'Paralithodes camtschaticus' #'Hippoglossus stenolepis' # 'Hippoglossoides elassodon' # 'Crangon dalli' # 'Ammodytes hexapterus' # 'Theragra chalcogramma' # 'Telmessus cheiragonus' # 'Tellina lutea' # 'Platichthys stellatus' # 'Oregonia gracilis' # 'Mallotus villosus' # 'Limanda proboscidea' # 'Limanda aspera' # 'Hyas lyratus' # 'Hippoglossus stenolepis' # 'Glyptocephalus zachirus' #'Gadus macrocephalus' #'Clupea pallasii pallasii' #'Aforia circinata'
time = 'none'
subset = data_subset(data,species,time)

# find max and min lats and longs of Asterias amurensis observations
min_lat = min([x.latitude for x in subset])
max_lat = max([x.latitude for x in subset])
min_long = min([x.longitude for x in subset])
max_long = max([x.longitude for x in subset])

# try out different parameter values on the 1985 data set to see which works best
"""
for i in frange(0.1,2,0.01):
	print(i, clusters(data,species,1985,i))
plot_set(data,species,1985)
"""

# test different parameter values over the different years
"""
for year in range(1984,2015):
	print("-----------------------")
	print("-----------------------")
	print("YEAR:", year)
	for i in frange(0.2,1.5,0.1):
		print(i, clusters(data,species,year,i))
	plot_set(data_subset(data,species,year))
"""

# visualize clustering for parameter=1.0

"""
for year in range(1984,2015):
	plot_clusters(data_subset(data,species,year),1.0)
"""

# animate each species
species_list = []
for x in data:
	if x.species not in species_list:
		print(x.species)
		species_list.append(x.species)

for species in species_list:
	animate(data_subset(data,species,time))



# https://github.com/mstrosaker/hclust/wiki/User's-guide
# https://stackoverflow.com/questions/28269157/plotting-in-a-non-blocking-way-with-matplotlib
# https://docs.scipy.org/doc/scipy-0.19.1/reference/generated/scipy.spatial.distance_matrix.html
# https://docs.scipy.org/doc/scipy/reference/generated/scipy.cluster.hierarchy.fclusterdata.html#scipy.cluster.hierarchy.fclusterdata
