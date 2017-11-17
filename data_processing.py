import csv
import math
from graphics import *
import matplotlib.pyplot as plt
from scipy.cluster import hierarchy

# class - observation datum
class observation(object):

	def __init__(self, index, species, longitude, latitude, year):
		self.index = int(index)
		self.species = species
		self.longitude = float(longitude)
		self.latitude = float(latitude)
		self.year = int(year)

	def toString(self):
		print(self.index, self.species, self.latitude, self.longitude)

# function - create subset of observations that are of given species in given year
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

# function to plot one data set (all observations of one species in one year)
def plot_set(data,species,year):
	data_set = data_subset(data,species,year)
	plt.scatter([x.longitude for x in data_set], [x.latitude for x in data_set])
	plt.axis([min_long - 1, max_long + 1, min_lat - 1, max_lat + 1])
	plt.show()

# =creates animation of observations of a certain species over the years
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
def clusters(data,species,year,param=1):
	radius = 100
	points = [[x.longitude, x.latitude] for x in data_subset(data,species,year)]
	print(len(points))
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

###############################################################################

# open and read data from file
data = []
with open("mydata.csv", "r") as csvfile:
	r = csv.reader(csvfile, delimiter=",")
	for row in r:
		x = observation(row[0], row[2], row[7], row[8], row[12])
		data.append(x)

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

# test the parameter value over the data over the years
param = 1
for year in range(1984,2015):
	print(clusters(data,species,year,param))
	plot_set(data,species,year)

# https://github.com/mstrosaker/hclust/wiki/User's-guide
# https://stackoverflow.com/questions/28269157/plotting-in-a-non-blocking-way-with-matplotlib
# https://docs.scipy.org/doc/scipy-0.19.1/reference/generated/scipy.spatial.distance_matrix.html
