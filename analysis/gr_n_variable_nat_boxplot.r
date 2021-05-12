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
# Filter dr for only Results
#------------------------------------------------
d <- dr %>%
  filter(resultConcerns=="Results")

#------------------------------------------------
# factor for box plot
#------------------------------------------------
timesNumber<- factor(d$n) # for boxPlot

#------------------------------------------------
# Draw the graph
#------------------------------------------------
d %>%
  ggplot(aes(x = timesNumber, y = (makespan/LowBound), color=algoName, shape=algoName))+
  geom_boxplot()+
  facet_grid(d$m ~ d$generateMethode)
  labs(
    title = "Comparison",
      y = "Normalized Makespan Cmax/Optimal"
  )
#------------------------------------------------
# Save graph in pdf file
#------------------------------------------------
ggsave(file = "gr_n_variable_nat_boxplot.pdf")

