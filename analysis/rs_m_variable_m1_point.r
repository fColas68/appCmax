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
  filter(resultConcerns=="m1Results")

#------------------------------------------------
# Draw the graph
#------------------------------------------------
d %>%
  # filter(resultConcerns=="m1Results") %>%
  ggplot(aes(x = m, y = (makespan/m1Optimal), color=algoName, shape=algoName))+ # , shape=algoName))+
  #ggplot(aes(x = n, y = (makespan), color=algorithm, shape=algorithm))+
  geom_point()+
  #geom_smooth(formula = y ~ x,  method=loess, se=FALSE)+
  #geom_smooth(formula = y ~ x, method=lm, se=FALSE)+
  geom_line() + 
  facet_grid(d$n ~ d$generateMethode)+
  labs(
    title = "Comparaison sur 5 PWA",
    y = "Makespan relatif"
  )

  ggsave(file = "rr_m_var_m1_point.pdf")

