from clustering import *
from plotting import *
import math

# Set species
my_species = "Aforia circinata"

class cluster(object):

	def __init__(self,ob,sp,ind,yr):
		self.observations = ob  # Array of observation data points in the cluster
		self.species = sp  # Species of the observations
		self.id = ind  # Index number of the cluster
		self.year = yr  # Year in which the cluster is found
		self.centroid = self.calc_centroid()  # The centroid of the cluster

	# Print identifying information of the cluster
	def cprint(self):
		print(self.year,self.id,self.species,len(self.observations),self.centroid)

	# Calculate the centroid of the cluster
	def calc_centroid(self):
		# Variables to track sums of latitudes and longitudes, and number of points
		sum_long = 0.0
		sum_lat = 0.0
		n = 0.0

		# Sum latitudes and longitudes for given cluster_id
		for x in self.observations:
			n += 1.0
			sum_long += x.longitude
			sum_lat += x.latitude

		# Compute and return component averages
		avgs = [sum_long / n, sum_lat / n]
		return avgs


##############################################################################

"""
Creates cluster objects for all years of observations of one species
Input: observations of given species across all years
Output: array of arrays of cluster objects for each year
"""
def make_clusters(data):

	cluster_dict = {}

	for year in range(1984,2015):

		year_subset = data_subset(data,"none",year)
		year_clustering = clusters(year_subset)

		year_array = []

		if year_clustering != 0:
			n_clusters = max(year_clustering) + 1

			# Loop thru cluster_id values
			for i in range(max(year_clustering)+1):
				obs = []
				# Loop thru elements of clustering array
				for j in range(len(year_clustering)):
					if year_clustering[j] == i:
						obs.append(year_subset[j])
				year_array.append(cluster(obs,my_species,i,year))  # Create new cluster if the current id is found
				
		cluster_dict[year] = year_array

	return cluster_dict


"""
Matches clusters from current year to clusters from next year
Input: current year, set of observations of given species
Output: array of indices that the nth current_year cluster maps to in next_year. so output[i] is the new-year cluster id that the ith current cluster maps to
"""
def cluster_map(current_year,data):

	# Find data sets and clusterings for current and next years
	current_subset = data_subset(data,"none",current_year)
	next_subset = data_subset(data,"none",current_year+1)
	current_clusters = make_clusters(data)[current_year]  # List of clusters from current year
	next_clusters = make_clusters(data)[current_year+1]  # List of clusters from next year

	# Return absence / extinction / colonization if necessary
	if len(current_subset) == 0 and len(next_subset) == 0:
		return "absence"
	elif len(current_subset) != 0 and len(next_subset) == 0:
		return "extinction"
	elif len(current_subset) == 0 and len(next_subset) != 0:
		return "colonization"

	# Minimum number of clusters present in either year
	n_clusts = min(len(current_clusters),len(next_clusters))

	# Make arrays of current and next centroids
	current_centroids = [clust.centroid for clust in current_clusters]
	next_centroids = [clust.centroid for clust in next_clusters]

	# Calculate pairwise distances between cluster centroids
	distance_arrays = []  # Each row is the set of distances from one current centroid to all new centroids
	for c in range(len(current_centroids)):  # Iterate thru current centroids
		distances = []
		for n in range(len(next_centroids)):  # Iterate thru next-year centroids
			current_c = current_centroids[c]
			next_c = next_centroids[n]
			dist = math.sqrt((current_c[0] - next_c[0]) ** 2 + (current_c[1] - next_c[1]) ** 2)  # Magnitude of displacement
			distances.append(dist)
		distance_arrays.append(distances)

	# Figure out which new cluster each current cluster should map to
	mapped_ids = []
	for i in range(len(distance_arrays)):
		m = distance_arrays[i].index(min(distance_arrays[i]))
		mapped_ids.append(m)

	print(mapped_ids)

	# Create dictionary out of this; key is current-year-cluster obj, value is next-year-cluster obj that it maps to
	cluster_dict = {}
	for i in range(len(current_clusters)):
		cluster_dict[current_clusters[i]] = next_clusters[mapped_ids[i]]

	return cluster_dict


def build_tree():
	return 0
	# Figure out how to put cluster_map maps into tree form


############### MAIN ############################################