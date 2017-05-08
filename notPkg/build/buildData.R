library(trawlData)
library(trawlDiversity)
library(spatialDiversity)



ebs_dat <- trawlDiversity::data_all[reg=='ebs']
ebs_sppMaster <- trawlDiversity::spp_master[reg=='ebs']
mapOwin <- trawlDiversity::mapOwin

save(ebs_dat, file="../data/ebs_dat.RData")
save(ebs_sppMaster, file="../data/ebs_sppMaster.RData")
save(mapOwin, file="../data/mapOwin.RData")