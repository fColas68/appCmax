#! /usr/bin/Rscript --vanilla
library(readr)
library(dplyr) # to use  %>% notation
library(ggplot2)

#------------------------------------------------
#init workspace
#------------------------------------------------
rm(list=ls())

#------------------------------------------------
# Reading file
#------------------------------------------------
#f <- file.choose(new = FALSE)
f <- "result.csv"
dr <- read_csv(file = f)

#------------------------------------------------
# Filter dr for only m1Results
#------------------------------------------------
d <- dr %>%
  filter(resultConcerns=="m1Results")

#------------------------------------------------
# factor for box plot
#------------------------------------------------
timesNumber <- factor(d$n)        # for boxPlot
# an          <- factor(d$algoName)

#------------------------------------------------
# Draw the graph in box plot
#------------------------------------------------
d %>%
  ggplot(aes(x = timesNumber, y = (makespan/m1Optimal), color=algoName, shape=algoName))+
  #ggplot(aes(x = timesNumber, y = (makespan-m1Optimal), color=algoName, shape=algoName))+
  geom_boxplot()+
  facet_grid(d$m ~ d$generateMethode)
  labs(
    title = "Comparison",
    y = "Normalized Makespan Cmax/Optimal"
  )

#------------------------------------------------
# Save graph in pdf file
#------------------------------------------------
ggsave(file = "rr_n_var_m1_boxplot.pdf")
  