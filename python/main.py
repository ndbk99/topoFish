from clustering import *
from plotting import *
from cluster_tracking import *

# list of species that exhibit clustering behavior
clustered_species = ['Aforia circinata','Argis dentata', 'Argis lar', 'Artediellus pacificus', 'Buccinum polare', 'Ciliatocardium ciliatum', 'Crangon dalli', 'Cyanea capillata', 'Echinarachnius parma', 'Elegius gracilis', 'Eunoe depressa', 'Euspira pallida', 'Gersemia rubiformis', 'Glebocarcinus oregonensis', 'Grandicrepidula grandis', 'Halichondria panicea', 'Halocynthia aurantium', 'Hiatella arctica', 'Icelus spatula', 'Icelus spiniger', \
'Leptasterias groenlandica', 'Limanda sakhalinensis', 'Liparis gibbus', 'Lycodes raridens', 'Mactromeris polynyma', 'Matridium farcimen', 'Musculus discors', 'Neocrangon communis', 'Ophiura sarsii', 'Pyrulofusus melonis', 'Rhamphostomella costata', 'Serratiflustra serrulata', 'Siliqua alta', 'Stomphia coccinea', 'Tellina lutea', 'Trichodon trichodon', 'Triglops pingelii', 'Triglops scepticus', 'Tritonia diomedea', 'Urticina crassicornis', 'Volutopsius fragilis', 'Volutopsius middendorffii']

########################## MAIN #######################################################

# Read data into observation objects, make species subset, make cluster objects
data = read_data("ebs_data.csv")
subset = data_subset(data,my_species,"none")


"""
# Print cluster mapping for each year
for year in range(1984,2014):
	print("YEAR:",year,"\n------------")
	cluster_dict = cluster_map(year,subset)

	if type(cluster_dict) is str:
		print(cluster_dict,"\n\n")
	else:
		for x in cluster_dict:
			x.cprint()  # Print current cluster
			cluster_dict[x].cprint()  # Print corresponding next cluster
			print("-")
		print(" ")
"""

animate_clusters(subset,0.5)  # animate clusters over the years

build_tree(subset)
