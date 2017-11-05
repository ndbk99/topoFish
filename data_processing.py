import csv
import math
from graphics import *

# class to hold observation data
class observation(object):
	def __init__(self, index, species, latitude, longitude, year):
		self.index = int(index)
		self.species = species
		self.latitude = float(latitude)
		self.longitude = float(longitude)
		self.year = int(year)

	def toString(self):
		print(self.index, self.species, self.latitude, self.longitude)

# creates subset of observations that are of given species in given year
def data_subset(data,species,year):
	result = []
	for x in data:
		if x.species == species and x.year == year:
			result.append(x)
	return result

# open and read data from file
data = []
with open("mydata.csv", "r") as csvfile:
	r = csv.reader(csvfile, delimiter=",")
	for row in r:
		x = observation(row[0], row[2], row[7], row[8], row[12])
		data.append(x)

# create subset of data
asterias_1984 = data_subset(data,'Asterias amurensis',1984)

# find max and min lats and longs of Asterias amurensis observations
min_lat = min([x.latitude for x in asterias])
max_lat = max([x.latitude for x in asterias])
min_long = min([x.longitude for x in asterias])
max_long = max([x.longitude for x in asterias])
width = max_long - min_long
height = max_lat - min_lat
print(width, height)

# normalize and scale coordinates
for x in asterias:
	x.latitude -= min_lat
	x.longitude -= min_long
	x.latitude *= 100
	x.longitude *= 100

# create graph window
win = GraphWin("topoFish",width*100, height*100)

# plot points in data selection
for x in asterias:
	p = Point(abs(x.latitude), x.longitude)
	print(x.index,x.latitude, x.longitude)
	p.setOutline("black")
	p.draw(win)


