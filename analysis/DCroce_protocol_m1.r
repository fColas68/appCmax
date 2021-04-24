echo =FALSE
library(readr)
library(dplyr) # to use  %>% notation
library(ggplot2)

#------------------------------------------------
# Reading file
#------------------------------------------------
f <- "result.csv"
data <- read_csv(file = f)

d <- data %>%
  filter(resultConcerns=="m1Results")

#------------------------------------------------
# Data D sort by generateMethod, [a-b] m id -> DS
#------------------------------------------------
ds <- d[order(d$generateMethode,d$`[a-b]`,d$m, d$id, d$makespan),]

#=============================
nb_raws <- dim(ds)[1]

#=============================
generateMethod_EnCours = ""
ab_Encours             = ""
m_EnCours              = 0
id_EnCours             = 0

results    <- tibble()
result_raw <-tibble(generateMethod=NA,'[a-b]'=NA, m=NA,
                    SLACK_vs_LPT_W=NA,   SLACK_vs_LPT_E=NA,   SLACK_vs_LPT_L=NA,
                    SLACKvsCOMBINE_W=NA, SLACKvsCOMBINE_E=NA, SLACKvsCOMBINE_L=NA,
                    SLACK_vs_LDM_W=NA,   SLACK_vs_LDM_E=NA,   SLACK_vs_LDM_L=NA)

#=============================
nSLACK_vs_LPT_W = 0
nSLACK_vs_LPT_E = 0
nSLACK_vs_LPT_L = 0
#
nSLACK_vs_LDM_W = 0
nSLACK_vs_LDM_E = 0
nSLACK_vs_LDM_L = 0
#
nSLACK_vs_COMBINE_W = 0
nSLACK_vs_COMBINE_E = 0
nSLACK_vs_COMBINE_L = 0
#
nLPT       = 0
nSLACK     = 0
nCOMBINE   = 0
nLDM       = 0


for (i in seq.int(nb_raws)){
  #==================================================
  #RUPTURE generationMethod | [a-b] | m (inextenso ID
  #==================================================
  if (generateMethod_EnCours != ds$generateMethode[i]|
      ab_Encours != ds$`[a-b]`[i]|
      m_EnCours != ds$m[i]) { 

    #------------------------------------------------
    # add the raw in dataframe results
    #------------------------------------------------
    if (generateMethod_EnCours != ""|
        ab_Encours != ""|
        m_EnCours != 0) { 
      #
        
      result_raw <-tibble(generateMethod=generateMethod_EnCours,'[a-b]'=ab_Encours, m=m_EnCours,
                          SLACK_vs_LPT_W    = nSLACK_vs_LPT_W,    SLACK_vs_LPT_E     = nSLACK_vs_LPT_E,    SLACK_vs_LPT_L    = nSLACK_vs_LPT_L,
                          SLACK_vs_COMBINE_W= nSLACK_vs_COMBINE_W,SLACK_vs_COMBINE_E = nSLACK_vs_COMBINE_E,SLACK_vs_COMBINE_L= nSLACK_vs_COMBINE_L,
                          SLACK_vs_LDM_W    = nSLACK_vs_LDM_W,    SLACK_vs_LDM_E     = nSLACK_vs_LDM_E,    SLACK_vs_LDM_L    = nSLACK_vs_LDM_L)
      #
      results<-rbind(results,result_raw)  
    } # if (generateMethod_EnCours != ""|
    
    #------------------------------------------------
    # New raw
    #------------------------------------------------
    generateMethod_EnCours = ds$generateMethode[i]
    ab_Encours             = ds$`[a-b]`[i]
    m_EnCours              = ds$m[i]
    id_EnCours             = ds$id[i]
    #
    nSLACK_vs_LPT_W         = 0
    nSLACK_vs_LPT_E         = 0
    nSLACK_vs_LPT_L         = 0
    #
    nSLACKvsCOMBINE_W       = 0
    nSLACKvsCOMBINE_E       = 0
    nSLACKvsCOMBINE_L       = 0
    #
    nSLACK_vs_LDM_W         = 0
    nSLACK_vs_LDM_E         = 0
    nSLACK_vs_LDM_L         = 0
    #
    nLPT       = 0
    nSLACK     = 0
    nCOMBINE   = 0
    nLDM       = 0
    
  }
  
  
  #==================================================
  # RUPTURE id --> give results (wo win !)
  #==================================================
  if (id_EnCours != ds$id[i]){
    #
    if (nSLACK <  nLPT)     {nSLACK_vs_LPT_W = nSLACK_vs_LPT_W+1}
    if (nSLACK == nLPT)     {nSLACK_vs_LPT_E = nSLACK_vs_LPT_E+1}
    if (nSLACK >  nLPT)     {nSLACK_vs_LPT_L = nSLACK_vs_LPT_L+1}
    #
    if (nSLACK <  nCOMBINE) {nSLACK_vs_COMBINE_W = nSLACK_vs_COMBINE_W+1}
    if (nSLACK == nCOMBINE) {nSLACK_vs_COMBINE_E = nSLACK_vs_COMBINE_E+1}
    if (nSLACK <  nCOMBINE) {nSLACK_vs_COMBINE_L = nSLACK_vs_COMBINE_L+1}
    #
    if (nSLACK <  nLDM)     {nSLACK_vs_LDM_W = nSLACK_vs_LDM_W+1}
    if (nSLACK == nLDM)     {nSLACK_vs_LDM_E = nSLACK_vs_LDM_E+1}
    if (nSLACK <  nLDM)     {nSLACK_vs_LDM_L = nSLACK_vs_LDM_L+1}

    id_EnCours <- ds$id[i]
    #
    nLPT       = 0
    nSLACK     = 0
    nCOMBINE   = 0
    nLDM       = 0
  } # if (id_EnCours != ds$id[i]){
  
  #==================================================
  # MAIN CASE
  #==================================================
  if (ds$algoName[i] == "LPT")     {nLPT         = ds$makespan[i]}
  if (ds$algoName[i] == "SLACK")   {nSLACK     = ds$makespan[i]}
  if (ds$algoName[i] == "COMBINE") {nCOMBINE = ds$makespan[i]}
  if (ds$algoName[i] == "LDM")     {nLDM         = ds$makespan[i]}

} # for (i in seq.int(nb_raws)){

result_raw <-tibble(generateMethod=generateMethod_EnCours,'[a-b]'=ab_Encours, m=m_EnCours,
                    SLACK_vs_LPT_W    = nSLACK_vs_LPT_W,    SLACK_vs_LPT_E     = nSLACK_vs_LPT_E,    SLACK_vs_LPT_L    = nSLACK_vs_LPT_L,
                    SLACK_vs_COMBINE_W= nSLACK_vs_COMBINE_W,SLACK_vs_COMBINE_E = nSLACK_vs_COMBINE_E,SLACK_vs_COMBINE_L= nSLACK_vs_COMBINE_L,
                    SLACK_vs_LDM_W    = nSLACK_vs_LDM_W,    SLACK_vs_LDM_E     = nSLACK_vs_LDM_E,    SLACK_vs_LDM_L    = nSLACK_vs_LDM_L)
#
results<-rbind(results,result_raw)  

#View(ds)
#View(results)


write.table(results, file = "dellaCroce.csv",
            sep = "\t", row.names = F)
