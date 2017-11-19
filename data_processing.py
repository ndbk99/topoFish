import csv
import math
from graphics import *
import matplotlib.pyplot as plt
from scipy.cluster import hierarchy

# observation datum
class observation(object):

	def __init__(self, index, species, longitude, latitude, year):
		self.index = int(index)
		self.species = species
		self.longitude = float(longitude)
		self.latitude = float(latitude)
		self.year = int(year)

	def toString(self):
		print(self.index, self.species, self.latitude, self.longitude)

# create subset of observations that are of given species in given year
def data_subset(data,species,year):

	result = []

	if species == "none":
		for x in data:
			if x.year == year:
				result.append(x)
	elif year == "none":
		for x in data:
			if x.species == species:
				result.append(x)
	else:
		for x in data:
			if x.species == species and x.year == year:
				result.append(x)

	return result

# plot one data set (all observations of one species in one year)
def plot_set(d):
	data_set = data_subset(data,species,year)
	plt.scatter([x.longitude for x in data_set], [x.latitude for x in data_set])
	plt.axis([min_long - 1, max_long + 1, min_lat - 1, max_lat + 1])
	plt.show()

# plot data set colored by cluster
def plot_clusters(d,clustering):

	# can't perform clustering on 0 or 1 points so exit function
	if len(d) < 2:
		plt.show()
		return 0

	plt.axis([min_long - 1, max_long + 1, min_lat - 1, max_lat + 1])

	for i in range(len(d)):

		cluster = clustering[i]

		if cluster % 4 == 0:
			c = "red"
		elif cluster % 4 == 1:
			c = "blue"
		elif cluster % 4 == 2:
			c = "green"
		elif cluster % 4 == 3:
			c = "black"

		plt.scatter(d[i].longitude, d[i].latitude, color=c)

	plt.show()

# create animation of observations of a certain species over the years
def animate(data):

	plt.ion()  # set plotting mode to interactive or whatever
	plt.show()

	# animate data from year to year
	i = 1
	for year in range(1984,2015):

		year_subset = data_subset(data,species,year)
		print(year)

		# plot and scale current figure
		fig = plt.figure(i)
		plt.scatter([x.longitude for x in year_subset], [x.latitude for x in year_subset])
		plt.axis([min_long - 1, max_long + 1, min_lat - 1, max_lat + 1])

		# draw and then clear current points
		plt.draw()
		plt.pause(0.1)
		plt.clf()

# find the cluster distribution for a data set
def clusters(d,param=1):
	points = [[x.longitude, x.latitude] for x in d]
	if len(points) > 1:
		clusters = hierarchy.fclusterdata(points,param)
		return clusters
	else:
		return 0

# modified range function to allow floats - used to test out different param values in fclusterdata
def frange(start, stop, step):
	result = []
	i = start
	while i < stop:
		yield i
		i += step
		result.append(i)
	return result

# open and read data from file
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
species = 'Aforia circinata'
year = 'none'
subset = data_subset(data,species,year)

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
for year in range(1984,2015):
	plot_clusters(data_subset(data,species,year),clusters(data_subset(data,species,year),1.0))

# https://github.com/mstrosaker/hclust/wiki/User's-guide
# https://stackoverflow.com/questions/28269157/plotting-in-a-non-blocking-way-with-matplotlib
# https://docs.scipy.org/doc/scipy-0.19.1/reference/generated/scipy.spatial.distance_matrix.html
# https://docs.scipy.org/doc/scipy/reference/generated/scipy.cluster.hierarchy.fclusterdata.html#scipy.cluster.hierarchy.fclusterdata
