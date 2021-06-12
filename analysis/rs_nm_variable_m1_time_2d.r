#! /usr/bin/Rscript --vanilla

library(readr)
library(dplyr) # to use  %>% notation
library(ggplot2)
library(metR)

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
  filter(resultConcerns=="m1Results" & m1_n > m & algoName=="SLACK")

#------------------------------------------------
# Draw the graph
# X --> Jobs number
# Y --> Machines number
# Z --> relative Makespan
#------------------------------------------------
#------------------------------------------------
# Draw the graph
# X --> Jobs number (m1)
# Y --> Machines number
# Z --> relative Makespan Cmax/Optimal
#------------------------------------------------

X <- d$m1_n
Y <- d$m
Z <- (d$makespan/d$m1Optimal)
T <- d$time
algoName <- d$algoName
generateMethode <- d$generateMethode
#d$mn <- factor(d$makespan/d$m1Optimal)
#d %>%
df <- data.frame(X,Y,Z, algoName, generateMethode)
#==================================
# preparing data for heat
#==================================
df %>%
  #==================================
  #
  #==================================
  ggplot(aes(x=X,y=Y,color=Z))+
  geom_point()+
  
  #==================================
  # COLOURS
  #==================================
  #scale_color_viridis()+
  scale_colour_viridis_c(option = "H")+
  #==================================
  # della Croce points
  #==================================
  #geom_point(aes(x=10,  y=5), colour="red", size=1)+
  #geom_point(aes(x=50,  y=5), colour="red", size=1)+
  #geom_point(aes(x=100, y=5), colour="red", size=1)+
  #geom_point(aes(x=500, y=5), colour="red", size=1)+
  #geom_point(aes(x=1000,y=5), colour="red", size=1)+
  #geom_point(aes(x=50,  y=10),colour="red", size=1)+
  #geom_point(aes(x=100, y=10),colour="red", size=1)+
  #geom_point(aes(x=500, y=10),colour="red", size=1)+
  #geom_point(aes(x=1000,y=10),colour="red", size=1)+
  #geom_point(aes(x=50,  y=25),colour="red", size=1)+
  #geom_point(aes(x=100, y=25),colour="red", size=1)+
  #geom_point(aes(x=500, y=25),colour="red", size=1)+
  #geom_point(aes(x=1000,y=25),colour="red", size=1)+
  
  #==================================
  # grid comparison
  #==================================
  facet_grid(generateMethode~.)
