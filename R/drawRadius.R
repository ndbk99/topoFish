#' drawRadius
#' 
#' Draw a radius around a point, or points
#' 
#' @param x,y coordinates of points in longitude latitude
#' @param rsize size of radius in km
#' @param ... arguments to pass to \code{\link{polygon}}
#' 
#' @return invisibly returns NULL
#' 
#' @details from http://stackoverflow.com/a/34187454/2343633
#' 
#' @examples
#' x <- -140:-170
#' y <- 15:45
#' plot(x, y)
#' drawRadius(x, y, 100)
#' 
#' @export
drawRadius <- function(x, y, rsize, ...){
	
	angle <- seq(0, 2*pi, length.out=100)
	
	circFun <- function(x,y){
		x2 <- x + (rsize /111 / cos(y/57.3)) * cos(angle)
		y2 <- y + (rsize / 111) * sin(angle)
		data.table(lon=x2, lat=y2)
	}
	
	circle_list <- mapply(circFun, x, y, SIMPLIFY=FALSE)
	
	dots <- list(...)
	for(l in 1:length(circle_list)){
		tcl <- circle_list[[l]]
		# tcl[,lines(lon, lat, ...)]
		tx <- tcl[,c(lon,rev(lon)[1])]
		ty <- tcl[,c(lat,rev(lat)[1])]
		do.call('polygon', args=c(list(x=tx, y=ty), dots))
	}
	
	invisible(NULL)
		
}

