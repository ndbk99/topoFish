import csv
import math
from graphics import *

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

# function - plot observation point on window
def plot(window,info=False):

	p = Point(x.longitude,abs(x.latitude))
	c = Circle(p,5)
	if info:
		print(x.index,x.longitude,x.latitude)
	c.setOutline("black")
	c.draw(window)

	return c


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

# calculate and scale window dimensions, allow for border padding
width = abs(max_long - min_long)*100 + 10
height = abs(max_lat - min_lat)*100 + 10
print(width, height)

# adjust coordinates
for x in subset:
	# normalize with minima
	x.latitude -= min_lat
	x.longitude -= min_long
	# scale
	x.latitude *= 100
	x.longitude *= 100
	# allow for border padding
	x.latitude += 5
	x.longitude += 5
	# flip right side up
	x.latitude = height - x.latitude

# create graph window
win = GraphWin("topoFish",width,height)

# plot points for each year for this species
for year in range(1984,2015):

	scatter = []  # array to hold graphics objects plotted


	# plot this round of points
	year_subset = data_subset(subset,'none',year)
	for x in year_subset:
		scatter.append(plot(win,x))

	# time delay
	for x in range(5000):
		Point(-10,-10).draw(win)

	# undraw this round of points
	for x in scatter:
		x.undraw()


# sketchy thing that keeps window open til you close it, and doesn't throw error on close
while win.isOpen():
	Point(-10,-10).draw(win)


################################################################################


# Okay I really need to get some better plotting library. Probably matplotlib is the way to go tbh and then I could not do all the scaling shite. Next step!
# 1) transition to matplotlib
# 2) create animations
# 3) implement best cluster-id method
# 4) start thinking about cluster-tracking problem