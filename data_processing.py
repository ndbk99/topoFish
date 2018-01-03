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
		plt.axis([min([x.longitude for x in data]) - 1, max([x.longitude for x in data]) + 1, min([x.latitude for x in data]) - 1, max([x.latitude for x in data]) + 1])

		# draw and then clear current points
		plt.draw()
		plt.pause(0.00005)
		plt.clf()

	plt.close()

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
			x = observation(row[0], row[2], row[7], row[8], int(row[12]))
			data.append(x)
	return data


###############################################################################

# read observation objects from data file
data = read_data("mydata.csv")

clustered_species = ['Aforia circinata','Argis dentata', 'Argis lar', 'Artediellus pacificus', 'Buccinum polare', 'Ciliatocardium ciliatum', 'Crangon dalli', 'Cyanea capillata', 'Echinarachnius parma', 'Elegius gracilis', 'Eunoe depressa', 'Euspira pallida', 'Gersemia rubiformis', 'Glebocarcinus oregonensis', 'Grandicrepidula grandis', 'Halichondria panicea', 'Halocynthia aurantium', 'Hiatella arctica', 'Icelus spatula', 'Icelus spiniger', \
'Leptasterias groenlandica', 'Limanda sakhalinensis', 'Liparis gibbus', 'Lycodes raridens', 'Mactromeris polynyma', 'Matridium farcimen', 'Musculus discors', 'Neocrangon communis', 'Ophiura sarsii', 'Pyrulofusus melonis', 'Rhamphostomella costata', 'Serratiflustra serrulata', 'Siliqua alta', 'Stomphia coccinea', 'Tellina lutea', 'Trichodon trichodon', 'Triglops pingelii', 'Triglops scepticus', 'Tritonia diomedea', 'Urticina crassicornis', 'Volutopsius fragilis', 'Volutopsius middendorffii']

for sp in clustered_species:
	animate(data,sp)
