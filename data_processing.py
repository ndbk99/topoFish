import csv
import math
import matplotlib.pyplot as plt
from scipy.cluster import hierarchy
import time as t

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
		cut = len(time) # - 6  # cut time of day out of timestamp string
		self.time = (t.strptime(time[0:cut], "%m/%d/%Y %H:%M")) # convert time into time.struct_time object

	def toString(self):
		print(self.index, self.species, self.latitude, self.longitude)

"""
create subset of observations that are of given species at given time
input: data to take subset of, name of species, time
output: set of observations that match the input parameters
"""
def data_subset(data,species,time="none"):

	result = []

	if time == "none":
		for x in data:
			if x.species == species:
				result.append(x)
	else:
		for x in data:
			if x.species == species and timeToString(x.time) == time:
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
input: set of observations of 1 species over all times, list of times (in time.struct_time object format) that observations of this species were made
output: animated plot of the species over the times
"""
def animate(data,times):

	# plt.ion()  # set plotting mode to interactive or whatever
	plt.show()

	# animate data from time to time
	i = 1
	for time in times:

		print(timeToString(time))
		time_subset = data_subset(data,species,timeToString(time))

		# plot current figure
		fig = plt.figure(i)
		plt.scatter([x.longitude for x in time_subset], [x.latitude for x in time_subset])
		plt.axis([min([x.longitude for x in data]) - 1, max([x.longitude for x in data]) + 1, min([x.latitude for x in data]) - 1, max([x.latitude for x in data]) + 1])

		# draw and then clear current points
		plt.draw()
		plt.pause(0.00005)
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
			x = observation(row[0], row[2], row[7], row[8], row[10])
			data.append(x)
	return data

"""
create sorted list of days of observations of a given species
input: set of observations of desired species
output: list of days that observations of that species were made
"""
def species_times(data):
	times = []
	for x in data:
		if x.time not in times:
			times.append(x.time)
	return sorted(times)

"""
convert time object to string
input: time object to be converted
output: string result
"""
def timeToString(time_object):
	return (t.strftime("%m/%d/%Y %H:%M",time_object))

###############################################################################

# read observation objects from data file
data = read_data("mydata.csv")

# create subset of data
species = 'Mactromeris polynyma'
subset = data_subset(data,species)

# animate the observations over time - actually just looks like one (sometimes 2) points dancing around. may not even need to cluster! could just take centroids and connect them or something
animate(subset, species_times(subset))
