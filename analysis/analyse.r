#------------------------------------------------
# Reading file
#------------------------------------------------
f <- "../results/pp2.csv"
#f <- file.choose(new = FALSE) #"../results/pp.csv"
data <- read.csv(file = f, header = FALSE)

#------------------------------------------------
# Working lists
#------------------------------------------------
lstPCH <- c(4,5,6,7,8,9)
lstCOLOR <- c("blue","red","green","yellow","cyan")
#lstCOLOR <- topo.colors(10)

#------------------------------------------------
# Filter, result with data$V9=="m1Results"
#------------------------------------------------
d <- subset(data, data$V9=="m1Results")

#------------------------------------------------
# Retrieve algo names list used in this csv file
#------------------------------------------------
algorithms <- levels(d$V10)
for (a in 1:length(algorithms)){
  algo <-subset(d, d$V10==algorithms[a])
  plot(algo$V6, algo$V12-algo$V8, main = "title", xlab = "jobs number", ylab = "normalized Cmax (C-opt)", type = "o", col = lstCOLOR[a], pch = lstPCH[a], lab = c(10, 5, 0)) 
  #title(algorithms[a])
  par(new=T)
}
par(new=F)

# LEGEND
legend("topleft", legend=algorithms,col=lstCOLOR, pch = lstPCH, lty=1:2, cex=0.8, box.lty = 1)

# OLD CODE
#------------------------------------------------
# Create series
#------------------------------------------------
# LPT <- subset(d, d$V10=="LPT")
# title("LPT")
# SLACK <- subset(d, d$V10=="SLACK")
# LDM <- subset(d, d$V10=="LDM")

#------------------------------------------------
# GRAPHIC
#------------------------------------------------
# plot(LPT$V6, LPT$V12-LPT$V8, main = "title", xlab = "jobs number", ylab = "normalized Cmax", type = "o", col = "red", pch = 1, lab = c(10, 5, 0)) 
# par(new=T)
# plot(SLACK$V6, SLACK$V12-SLACK$V8, main = "title", xlab = "jobs number", ylab = "normalized Cmax", type = "o", col = "blue", pch = 3, lab = c(10, 5, 0)) 
# par(new=T)
# plot(LDM$V6, LDM$V12-LDM$V8, main = "title", xlab = "jobs number", ylab = "normalized Cmax", type = "o", col = "green", pch = 2, lab = c(10, 5, 0)) 
# par(new=F)

