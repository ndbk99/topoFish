#' plot map
#' 
#' plots a smoothed map of a value as a semi-transparent background w/ outline of sampled area and landmass map
#' 
#' @param x x coordinate
#' @param y y coordinate
#' @param marks value to be plotted
#' @param owin object for outline
#' @param zlim limits for the z (color) axis; useful for standardizing color scale across plots.
#' 
#' @return invisibly returns \code{NULL}
#' @export
plot_map <- function(x, y, marks, map_owin, zlim=NULL){
	requireNamespace("maps", quietly = TRUE)
	requireNamespace("raster", quietly = TRUE)
	requireNamespace("spatstat", quietly = TRUE)
	
	toRast <- function(p){
		requireNamespace("sp", quietly = TRUE)
		crs_orig <- sp::CRS("+proj=longlat")
	
		x0 = rep(p$xcol, length(p$yrow))
		y0 = rep(p$yrow, each=length(p$xcol))
		z = c(t(as.matrix(p)))
	
		r0 <- raster::rasterFromXYZ(cbind(x0, y0, z), crs=crs_orig)
		r <- r0
		return(r)
	}
	
	library(maps)
	mapPPP_ce <- spatstat::ppp(x=x, y=y, marks=marks, window=map_owin) 
	t_idw <- spatstat::Smooth(mapPPP_ce, hmax=1)
	z <- toRast(t_idw)
	if(is.null(zlim)){
		zlim <- range(z, na.rm=TRUE)
	}
	map_col <- grDevices::colorRampPalette(c("#000099", "#00FEFF", "#45FE4F", "#FCFF00", "#FF9400", "#FF3100"))(256)
	raster::image(z, col=adjustcolor(map_col, 0.25), xlab="", ylab="", asp=1, zlim=zlim)
	if(any(x < -180)){
		w2 <- maps::map('world2', plot=FALSE)
		w2$x <- w2$x-360
		maps::map(w2, add=TRUE, fill=TRUE, col="lightgray")
	}else{
		maps::map(add=TRUE, fill=TRUE, col="lightgray")
	}
	invisible(NULL)
}

