import matplotlib.pyplot as plt
from scipy.misc import imread

from clustering import *

############# PLOTTING #########################################################

plot_borders = [-175.5,-157.5,49.5,66.0]

def plot(points):
	plt.scatter([p[0] for p in points], [p[1] for p in points])
	plt.axis(plot_borders)
	# Show background image of Alaska map
	img = imread("map_adjusted.jpg")
	plt.imshow(img,zorder=0, extent=plot_borders)
	plt.show()

"""
Plot one data set (all observations of one species at one time)
Input: set of observations of 1 species at 1 time
Output: plot of data points
"""
def plot_set(data):
	plt.scatter([x.longitude for x in data], [x.latitude for x in data])
	plt.axis(plot_borders)
	# Show background image of Alaska map
	img = imread("map_adjusted.jpg")
	plt.imshow(img,zorder=0, extent=plot_borders)
	plt.show()

"""
Plot clusters of data
Input: set of observations of 1 species at 1 time
Output: plot of data points colored by cluster
"""
def plot_clusters(data):

	# Can't perform clustering on 0 or 1 points so exit function
	if len(data) < 1:
		plt.show()
		return 0

	# Otherwise, perform clustering
	clustering = clusters(data)

	plt.axis(plot_borders)
	# plt.axis([min_long - 1, max_long + 1, min_lat - 1, max_lat + 1])


	# Assign colors to cluster points
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

		# Plot colored points
		plt.scatter(data[i].longitude, data[i].latitude, color=c, zorder=1)

	# Show background image of Alaska map
	img = imread("map_adjusted.jpg")
	plt.imshow(img,zorder=0, extent=plot_borders)

	plt.show()
	plt.close()

"""
Create animation of observations of a certain species over the years
Input: set of observations of 1 species over all years
Output: animated plot of the species over the years
"""
def animate_set(data):

	plt.show()

	print(species)

	# Animate data for each year
	i = 1
	for time in range(1984,2015):

		time_subset = data_subset(data,"none",time)

		# Plot points for current year
		fig = plt.figure(i)
		plt.scatter([x.longitude for x in time_subset], [x.latitude for x in time_subset])
		plt.axis(plot_borders)
		# plt.axis([min([x.longitude for x in data]) - 1, max([x.longitude for x in data]) + 1, min([x.latitude for x in data]) - 1, max([x.latitude for x in data]) + 1])

		# Draw and then clear current points
		plt.draw()
		plt.pause(0.00005)
		plt.clf()

	plt.close()


"""
Animate clusters of data
Input: set of observations of 1 species over all times
Output: animation of clusters over time
"""
def animate_clusters(data,speed=0.001):

	plt.show()

	for year in range(1984,2015):

		# Create subset of data from that year
		subset = data_subset(data,"none",year)
		print(year) ###, "observations:",len(subset))

		# Create new figure
		fig = plt.figure(1)

		# Only perform clustering if there's more than one point
		if len(subset) >= 1:
			clustering = clusters(subset)
			for i in range(len(subset)):
				cluster = clustering[i]
				if cluster % 4 == 0:
					c = "red"
				elif cluster % 4 == 1:
					c = "blue"
				elif cluster % 4 == 2:
					c = "orange"
				elif cluster % 4 == 3:
					c = "black"

				# Plot point in color corresponding to cluster id
				plt.scatter(subset[i].longitude, subset[i].latitude, color=c, zorder=1)

		plt.axis(plot_borders)
		# Show background image of Alaska map
		img = imread("map_adjusted.jpg")
		plt.imshow(img,zorder=0, extent=plot_borders)

		# Draw and then clear current points
		plt.draw()
		plt.pause(speed)
		plt.clf()

	plt.close()
