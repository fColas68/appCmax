data <- read.csv(file = "../results/pp.csv", header = FALSE)
d <- subset(data, data$V9=="m1Results")
#LPT <- subset(d, d$V10=="LPT")
#SLACK <- subset(d, d$V10=="SLACK")
#LDM <- subset(d, d$V10=="LDM")
#algo <- d$V10
#algo

plot(d$V6, d$V12-d$V8, main = "title", xlab = "jobs number", ylab = "normalized Cmax", type = "p", col = "black", pch = 20, lab = c(10, 5, 0)) 
#plot(LPT$V6, LPT$V12-LPT$V8, main = "title", xlab = "jobs number", ylab = "normalized Cmax", type = "p", col = "blue", pch = 3, lab = c(10, 5, 0)) 
#plot(SLACK$V6, SLACK$V12-SLACK$V8, main = "title", xlab = "jobs number", ylab = "normalized Cmax", type = "p", col = "blue", pch = 3, lab = c(10, 5, 0)) 
#plot(LDM$V6, LDM$V12-LDM$V8, main = "title", xlab = "jobs number", ylab = "normalized Cmax", type = "p", col = "blue", pch = 3, lab = c(10, 5, 0)) 
#plot(d$V6, )






