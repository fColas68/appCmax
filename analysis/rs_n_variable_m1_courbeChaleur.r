#! /usr/bin/Rscript --vanilla

library(readr)
library(dplyr) # to use  %>% notation
library(ggplot2)
library(metR)


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
  filter(resultConcerns=="m1Results")

#------------------------------------------------
# Draw the graph
# X --> Jobs number
# Y --> Machines number
# Z --> relative Makespan
#------------------------------------------------
d %>%
  ggplot(aes(x=m1_n,y=m,color=(makespan/m1Optimal)))+
  geom_point()+
  # della Croce points
  geom_point(aes(x=10, y=5), colour="red")+
  geom_point(aes(x=50, y=5), colour="red")+
  geom_point(aes(x=100, y=5), colour="red")+
  geom_point(aes(x=500, y=5), colour="red")+
  geom_point(aes(x=1000, y=5), colour="red")+
  geom_point(aes(x=50, y=10), colour="red")+
  geom_point(aes(x=100, y=10), colour="red")+
  geom_point(aes(x=500, y=10), colour="red")+
  geom_point(aes(x=1000, y=10), colour="red")+
  geom_point(aes(x=50, y=25), colour="red")+
  geom_point(aes(x=100, y=25), colour="red")+
  geom_point(aes(x=500, y=25), colour="red")+
  geom_point(aes(x=1000, y=25), colour="red")+
  #geom_point(aes(x=299, y=150), colour="yellow")+
  # grid comparison
  facet_grid(d$algoName ~ d$generateMethode)

  
  
  
  
  
  #ggsave(file = "rr_n_var_m1_CourbeChal.pdf")
  #ggsave(file = "rr_n_var_m1_CourbeChal.jpg")

