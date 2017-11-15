import csv
import math
from graphics import *
import matplotlib.pyplot as plt

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

################################################################################

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

plt.ion()  # set plotting mode to interactice
plt.show()

# animate data from year to year
i = 1
for year in range(1984,2015):

	year_subset = data_subset(data,species,year)
	print(year)

	fig = plt.figure(i)
	plt.scatter([x.longitude for x in year_subset], [x.latitude for x in year_subset])
	plt.axis([min_long - 1, max_long + 1, min_lat - 1, max_lat + 1])

	plt.draw()
	plt.pause(0.1)
	plt.clf()

# https://stackoverflow.com/questions/28269157/plotting-in-a-non-blocking-way-with-matplotlib