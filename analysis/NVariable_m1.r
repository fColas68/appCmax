library(readr)
library(dplyr) # to use  %>% notation
library(ggplot2)

#------------------------------------------------
# Reading file
#------------------------------------------------
#f <- file.choose(new = FALSE)
f <- "../results/Recette_FCO_15042021/Recette_FCO_15042021.csv"
data <- read_csv(file = f)

d <- data %>%
  filter(resultConcerns=="m1Results")

#------------------------------------------------
# Draw the graph
#------------------------------------------------
d %>%
  # filter(resultConcerns=="m1Results") %>%
  ggplot(aes(x = n, y = (makespan/m1Optimal), color=algoName, shape=algoName))+
  #ggplot(aes(x = n, y = (makespan), color=algorithm, shape=algorithm))+
  geom_point()+
  geom_smooth(formula = y ~ x,  method=loess, se=FALSE)+
  # geom_smooth(formula = y ~ x, method=lm, se=FALSE)+
  # geom_line() + 
  facet_grid(d$m ~ d$generateMethode)
  labs(
    title = "Comparaison",
    y = "Makespan normalisé Cmax-optimal"
  )


  #------------------------------------------------
  # Filter, result with data$V9=="m1Results"
  #------------------------------------------------
  #d <- subset(data, data$resultConcerns=="m1Results")
  #------------------------------------------------
  # Factor management (for series)
  #------------------------------------------------
  # d$algorithm = as.factor(d$algoName)
  
  
