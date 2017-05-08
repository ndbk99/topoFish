update_dependencies <- function(){
	devtools::use_package("data.table", type="Depends") # Basis for handling all data sets
	
	
	devtools::use_package("rbLib", type="Imports") #rbatt github
	devtools::use_package("stats", type="Imports")
	devtools::use_package("methods", type="Imports")
	
	devtools::use_package("animation", type="Suggests")
	devtools::use_package("geosphere", type="Suggests")
	devtools::use_package("trawlData", type="Suggests") # on rbatt github
	devtools::use_package("raster", type="Suggests")
	
	devtools::use_package("maps", type="Suggests")
	devtools::use_package("viridis", type="Suggests")
	
	devtools::use_package("spatstat", type="Suggests")
	devtools::use_package("sp", type="Suggests")
	
}