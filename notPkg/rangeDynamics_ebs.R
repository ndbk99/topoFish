# =================
# = Load Packages =
# =================

library(topoFish)


# =============
# = Scripting =
# =============
lo <- matrix(rep(1, 9), ncol=3)
lo[1,1] <- 2


# ===========
# = options =
# ===========

radius_size <- 100
plot_convex_hull <- FALSE
plot_temp <- TRUE

uspp <- ebs_sppMaster[ce_categ=="both", unique(spp)]
# setwd("~/Documents/School&Work/pinskyPost/topoFish/notPkg")
old.wd <- getwd()
setwd("../notPkg/figures")
# for(us in 1:length(uspp)){
for(us in 1:1){
	tspp <- uspp[us]
	treg <- 'ebs' # eastern bering sea
	t_name <- paste0(treg, "_", gsub(" ", "_", tspp), ".gif") # file name
	
	spp_dat <- ebs_dat[spp==tspp]
	yr_range <- spp_dat[spp==tspp, range(year)]
	yr_dat <- ebs_dat[year>=yr_range[1] & year<=yr_range[2]]
	uy <- yr_dat[,sort(unique(year))]
	bg_dat <- yr_dat[!is.na(btemp)][!duplicated(paste(lon,lat))] # background data; unique lon-lat combinations, with bottom temperature
	animation::saveGIF(
		{
			animation::ani.options(inverval=0.0001)
			for(ty in 1:length(uy)){
				tyr <- uy[ty]
				tdat <- spp_dat[year==tyr] # data just for current year
				
				if(require("trawlData")){
					layout(lo) # set up figure layout so can add images more easily
				}
				if(plot_temp){
					bg_dat[year==tyr, plot_map(x=lon, y=lat, marks=btemp, map_owin=topoFish::mapOwin[[treg]])] # plot background colors
				}else{
					plot(topoFish::mapOwin[[treg]], main="")
					map(add=TRUE, fill=TRUE, col='lightgray')
				}
				
				
				nrtd <- nrow(tdat)
				if(nrtd > 1){
					combos <- CJ(1:nrtd, 1:nrtd)
					xdat <- tdat[combos[,V1], list(lon,lat)]
					ydat <- tdat[combos[,V2], list(lon,lat)]
					dists <- as.dist(matrix(geoDist(x=xdat, y=ydat), nrow=nrtd)) # geoDist is like Euclidean, but curvature of Earth
					clusts <- hclust(dists, method='single') # do hierarchical clustering
					groups <- cutree(clusts, h=radius_size) # h is the cutoff height from the dendrogram
					tdat[,clustGroup:=groups]
					tdat[,clustColor:=viridis::viridis(max(groups))[groups]]
					
					if(plot_convex_hull){
						tdat[, j={
							ch <- chull(x=lon, y=lat)
							ch <- c(ch, ch[1])
							.SD[ch,lines(list(x=lon,y=lat), col=clustColor)]
						} ,by=c("clustGroup")]
					}
					
				}else{
					tdat[,clustColor:='black']
					tdat[,clustGroup:=1]
				}
				
				# tdat[,points(lon, lat, pch=19, col='black', cex=1.5)]
				
				if(ty==1){t1_dat <- tdat}
				# t1_dat[,drawRadius(lon, lat, rsize=radius_size, col='lightgray')]
				if(nrow(t1_dat)>0){
					# t1_dat[,drawRadius(lon, lat, rsize=radius_size, border=NA, col=adjustcolor(clustColor, 0.1)),by='clustGroup']
				}
				if(nrow(tdat)>0){
					tdat[,drawRadius(lon, lat, rsize=radius_size, border=clustColor, col=adjustcolor(clustColor, 0.25)),by='clustGroup']
					tdat[,points(lon, lat, pch=21, bg=clustColor, cex=1.5)] # plot points where the species was observed
				}
				mtext(tyr, side=1, line=-1, font=2, adj=0.1)
				mtext(tspp, side=3, line=0.1, font=3, adj=0.9)
				
				if(require("trawlData")){
					trawlData::sppImg(tspp) # plot picture of critter
				}
				t1_dat <- tdat
			}
	
		},
		autobrowse=FALSE,
		ani.height=400,
		ani.width=400,
		movie.name=t_name,
	)
}
setwd(old.wd)