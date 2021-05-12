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
data <- read_csv(file = f)

d <- data %>%
  filter(resultConcerns=="Results")

#------------------------------------------------
# Draw the graph
#------------------------------------------------
d %>%
  # filter(resultConcerns=="m1Results") %>%
  ggplot(aes(x = m, y = (makespan/LowBound), color=algoName, shape=algoName))+
  #ggplot(aes(x = n, y = (makespan), color=algorithm, shape=algorithm))+
  geom_point()+
  geom_smooth(formula = y ~ x,  method=loess, se=FALSE)+
  #geom_smooth(formula = y ~ x, method=lm, se=FALSE)+
  geom_line() + 
  facet_grid(d$n ~ d$generateMethode)
  labs(
    title = "Comparaison",
    y = "Makespan normalisé Cmax-optimal"
  )

  ggsave(file = "gr_m_variable_nat_point.pdf")

