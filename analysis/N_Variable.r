library(ggplot2)
library(magrittr) # to use  %>% notation

#------------------------------------------------
# Reading file
#------------------------------------------------
#f <- "../results/testParam2_FCO_03042021.csv"
f <- file.choose(new = FALSE) #"../results/pp.csv"
data <- read.csv(file = f, header = TRUE)

#------------------------------------------------
# Working lists
#------------------------------------------------
lstPCH <- c(4,5,6,7,8,9)
lstCOLOR <- c("blue","red","green","yellow","cyan")


#------------------------------------------------
# Filter, result with data$V9=="m1Results"
#------------------------------------------------
d <- subset(data, data$resultConcerns=="m1Results")



#------------------------------------------------
# Factor management
#------------------------------------------------
#algorithms <- levels(d$algoName)
d$algorithm = as.factor(d$algoName)

#------------------------------------------------
# Draw the graph
#------------------------------------------------
d %>% ggplot()


d %>%
  ggplot(aes(x = n, y = (makespan/m1Optimal), color=algorithm, shape=algorithm))+
  #ggplot(aes(x = n, y = (makespan), color=algorithm, shape=algorithm))+
  geom_point()+
  geom_smooth(method=loess, se=FALSE)+
  #geom_smooth(method=lm)+
  geom_line() + 
  labs(
    title = "Comparaison",
    y = "Makespan normalisé Cmax-optimal"
  )



