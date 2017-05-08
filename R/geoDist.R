#' geographic distance
#' 
#' geographic distance between two sets of points
#' 
#' @param x,y length-2 (or 2-column object coercable to matrix) where the first element (or column) is longtitude, second is latitude
#' 
#' @return
#' returns the distance between \code{x} and \code{y}. If \code{x} and \code{y} have multiple rows, then returns a vector of the geographic distances between corresponding rows
#' 
#' @export
geoDist <- function(x, y){
	if(!is.null(nrow(x))){
		x <- as.matrix(x)
	}
	if(!is.null(nrow(y))){
		y <- as.matrix(y)
	}
	
	x180 <- x < -180
	x[x180] <- x[x180] + 360
	y180 <- y < -180
	y[y180] <- y[y180] + 360
	
	geosphere::distVincentyEllipsoid(x, y)/1E3
	
}