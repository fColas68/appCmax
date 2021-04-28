#! /usr/bin/Rscript --vanilla

library(readr)
library(dplyr) # to use  %>% notation
library(ggplot2)

#------------------------------------------------
# Reading file
#------------------------------------------------
#f <- file.choose(new = FALSE)
f <- "result.csv"
data <- read_csv(file = f)
timesNumber<- factor(d$n) # for boxPlot
an <- factor(d$algoName)

d <- data %>%
  filter(resultConcerns=="m1Results")

#------------------------------------------------
# Draw the graph
#------------------------------------------------
d %>%
  # filter(resultConcerns=="m1Results") %>%
  ggplot(aes(x = timesNumber, y = (makespan/m1Optimal), color=algoName, shape=algoName))+
  #ggplot(aes(x = n, y = (makespan), color=algorithm, shape=algorithm))+
  geom_boxplot()+
  facet_grid(d$m ~ d$generateMethode)
  labs(
    title = "Comparaison",
    y = "Makespan normalisé Cmax-optimal"
  )

  ggsave(file = "res_boxPlot_nVariable_m1.pdf")

