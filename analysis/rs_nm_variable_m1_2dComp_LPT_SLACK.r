#! /usr/bin/Rscript --vanilla
echo= FALSE
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
  filter(resultConcerns=="m1Results" & m1_n > m & (algoName =="SLACK" | algoName =="LPT" ))
#------------------------------------------------
# Data D sort by generateMethod, [a-b] m id -> DS
#------------------------------------------------
dfa <- d[order(d$m1_n,d$m, d$generateMethode, d$algoName),]

currentKey <- ""
sKey       <- ""

#==================================
# Cumulatives data frames
#==================================
# X Y generate ALgoName MakeSpan/Optimal For final  result
dfw   <- tibble()  # data.frame is obsolete

# X Y generateMethode aLgoName MakeSpan/Optimal
nX = NA
nY = NA
sGenerateMethode = NA
sAlgoName = NA
nMinRelativeMakespan = NA
#dfRow <- tibble(rX=nX, rY= nY, rGenerateMethode = sGenerateMethode, rAlgoName=sAlgoName , rMinRelativeMakespan = nMinRelativeMakespan)   
dfRow <- tibble(rX=NA, rY= NA, rGenerateMethode = NA, rAlgoName=NA , rMinRelativeMakespan = NA)  


#==================================
# Course of initial data frame
#==================================
currentKey <- ""
sKey       <- ""
for(i in 1:nrow(dfa)){
  #========================================
  # Current Key Value
  #========================================
  sKey = paste(dfa$m1_n[i],dfa$m[i],dfa$generateMethode[i],sep="")
  
  #========================================
  # RUPTURE
  #========================================
  
  
  
  if(currentKey != sKey){
    if(currentKey != "" ){
      #Cumulate
      dfw <- rbind(dfw, dfRow)
    }  

    # init row
    nX = dfa$m1_n[i]
    nY = dfa$m[i]
    sGenerateMethode = dfa$generateMethode[i]
    sAlgoName = dfa$algoName[i]
    nMinRelativeMakespan = NA
    dfRow <- tibble(rX=nX, rY= nY, rGenerateMethode = sGenerateMethode, rAlgoName=sAlgoName , rMinRelativeMakespan = nMinRelativeMakespan)
    head(dfRow)
    
    # init key rupture
    currentKey = sKey
  }
  head(dfRow)
  #========================================
  # USUAL CASE
  #========================================
  if (is.na(dfRow$rMinRelativeMakespan[1]) ) {
    dfRow$rMinRelativeMakespan[1]   <- (dfa$makespan[i]/dfa$m1Optimal[i])
    dfRow$rAlgoName[1]              <- dfa$algoName[i]
  }
  else {
    
    # this value is better than currant
    if( (dfa$makespan[i]/dfa$m1Optimal[i]) < dfRow$rMinRelativeMakespan[1]){
      dfRow$rMinRelativeMakespan[1] <- (dfa$makespan[i]/dfa$m1Optimal[i])
      dfRow$rAlgoName[1]            <- dfa$algoName[i]
    }
    else if ( (dfa$makespan[i]/dfa$m1Optimal[i]) == dfRow$rMinRelativeMakespan[1]){
      dfRow$rAlgoName[1]            <- "_ LPT et SLACK"
    }
  }
} # for(i in 1:length(dfa)){

# Last row
if(currentKey != ""){
  dfw <- rbind(dfw, dfRow)        
} #




dfw %>%
  #==================================
  #
  #==================================
  ggplot(aes(x=rX,y=rY,color=rAlgoName))+
  geom_point(size=1)+
  scale_color_manual(values=c("yellow", "blue", "green", "purple"))+
  
  #==================================
  # della Croce points
  #==================================
  geom_point(aes(x=10,  y=5), colour="red", size=1)+
  geom_point(aes(x=50,  y=5), colour="red", size=1)+
  geom_point(aes(x=100, y=5), colour="red", size=1)+
  geom_point(aes(x=500, y=5), colour="red", size=1)+
  geom_point(aes(x=1000,y=5), colour="red", size=1)+
  geom_point(aes(x=50,  y=10),colour="red", size=1)+
  geom_point(aes(x=100, y=10),colour="red", size=1)+
  geom_point(aes(x=500, y=10),colour="red", size=1)+
  geom_point(aes(x=1000,y=10),colour="red", size=1)+
  geom_point(aes(x=50,  y=25),colour="red", size=1)+
  geom_point(aes(x=100, y=25),colour="red", size=1)+
  geom_point(aes(x=500, y=25),colour="red", size=1)+
  geom_point(aes(x=1000,y=25),colour="red", size=1)+

  labs(
    title = "Comparaison entre LPT et SLACK",
    x = "nombre de jobs",
    y = "nombre de machines"
  )+

  #==================================
  # grid comparison
  #==================================
  facet_grid(rGenerateMethode~.)

  