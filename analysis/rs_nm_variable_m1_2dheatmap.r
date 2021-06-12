#! /usr/bin/Rscript --vanilla

library(readr)
library(dplyr) # to use  %>% notation
library(ggplot2)
library(metR)
library(reshape)
library(viridis)           # Charger

#------------------------------------------------
#init workspace
#------------------------------------------------
rm(list=ls())

#------------------------------------------------
# Reading file
#------------------------------------------------
#f <- file.choose(new = FALSE)
f <- "result.csv"
data <- read_csv(file = f)
d <- data %>%
  filter(resultConcerns=="m1Results" & m1_n > m)

#------------------------------------------------
# Draw the graph
# X --> Jobs number (m1)
# Y --> Machines number
# Z --> relative Makespan Cmax/Optimal
#------------------------------------------------

X <- d$m1_n
Y <- d$m
Z <- (d$makespan/d$m1Optimal)
Zc <- cut((d$makespan/d$m1Optimal), quantile(d$makespan/d$m1Optimal) )
#Z <- cut((d$makespan/d$m1Optimal), breaks = 150 )
algoName <- d$algoName
generateMethode <- d$generateMethode

df <- data.frame(X,Y,Z, Zc, algoName, generateMethode)



#==================================
# preparing data for heat
#==================================

#d$m1Mean <- cut(          (d$makespan/d$m1Optimal), 
#                              mean((d$makespan/d$m1Optimal)) )
df %>%
  ggplot()+
  geom_tile(aes(X, Y,fill = Zc))+
  geom_contour_fill(aes(fill = stat(level)))+
  
  
  scale_colour_gradientn(1
    colours = c("blue", "green", "yellow", "orange", "red"),
    #limits = c(0.1, 2.5),
    na.value = "transparent"
  )+

  
  # della Croce points
#  geom_point(aes(x=10,  y=5), colour="red")+
#  geom_point(aes(x=50,  y=5), colour="red")+
#  geom_point(aes(x=100, y=5), colour="red")+
#  geom_point(aes(x=500, y=5), colour="red")+
#  geom_point(aes(x=1000,y=5), colour="red")+
#  geom_point(aes(x=50,  y=10),colour="red")+
#  geom_point(aes(x=100, y=10),colour="red")+
#  geom_point(aes(x=500, y=10),colour="red")+
#  geom_point(aes(x=1000,y=10),colour="red")+
#  geom_point(aes(x=50,  y=25),colour="red")+
#  geom_point(aes(x=100, y=25),colour="red")+
#  geom_point(aes(x=500, y=25),colour="red")+
#  geom_point(aes(x=1000,y=25),colour="red")+
  # grid comparison
  facet_grid(algoName ~ generateMethode)
