echo =FALSE
library(readr)
library(dplyr) # to use  %>% notation
library(ggplot2)

#----------------------------------------------------------------------
# Reading file
#----------------------------------------------------------------------
f <- "result.csv"
data <- read_csv(file = f)

#----------------------------------------------------------------------
# Only M1_Results
#----------------------------------------------------------------------
d <- data %>%
  filter(resultConcerns=="m1Results")

#------------------------------------------------
# Data D sort by generateMethod, [a-b] m id -> DS
#------------------------------------------------
ds <- d[order(d$generateMethode,d$`[a-b]`,d$m, d$id, d$makespan),]

#------------------------------------------------
# Size of data fram
#------------------------------------------------
nb_raws <- dim(ds)[1]

#----------------------------------------------------------------------
# breaking variables
#----------------------------------------------------------------------
generateMethod_EnCours = ""
ab_Encours             = ""
m_EnCours              = 0
id_EnCours             = 0

#----------------------------------------------------------------------
# comparison MakeSpan part
#----------------------------------------------------------------------
mk_results    <- tibble() # data_frame is obsolete
mk_result_raw <-tibble(generateMethod=NA,'[a-b]'=NA, m=NA,
                       SLACK_vs_LPT_W=NA,   SLACK_vs_LPT_E=NA,   SLACK_vs_LPT_L=NA,
                       SLACKvsCOMBINE_W=NA, SLACKvsCOMBINE_E=NA, SLACKvsCOMBINE_L=NA,
                       SLACK_vs_LDM_W=NA,   SLACK_vs_LDM_E=NA,   SLACK_vs_LDM_L=NA)

#------------------------------------ Cumul
nSLACK_vs_LPT_W     = 0
nSLACK_vs_LPT_E     = 0
nSLACK_vs_LPT_L     = 0
#
nSLACK_vs_LDM_W     = 0
nSLACK_vs_LDM_E     = 0
nSLACK_vs_LDM_L     = 0
#
nSLACK_vs_COMBINE_W = 0
nSLACK_vs_COMBINE_E = 0
nSLACK_vs_COMBINE_L = 0
#------------------------------------ by Campaign ID
nLPT                = 0
nSLACK              = 0
nCOMBINE            = 0
nLDM                = 0

#----------------------------------------------------------------------
# comparison time part
#----------------------------------------------------------------------
tm_results    <- tibble() # data_frame is obsolete
tm_result_raw <-tibble(generateMethod=NA,'[a-b]'=NA, m=NA, SLACK=NA, LPT= NA, COMBINE=NA, LDM=NA)

#------------------------------------ Cumul
nTimeTot_LPT       = 0
nTimeTot_SLACK     = 0
nTimeTot_COMBINE   = 0
nTimeTot_LDM       = 0

for (i in seq.int(nb_raws)){
  ################################################################
  #
  #    RUPTURE generationMethod | [a-b] | m | (in extenso ID
  #
  ################################################################
  if (generateMethod_EnCours != ds$generateMethode[i]|
      ab_Encours != ds$`[a-b]`[i]|
      m_EnCours != ds$m[i]) { 

    #================================================
    # COMPUTE LAST BREAKING ID
    #================================================
    if (nSLACK <  nLPT)     {nSLACK_vs_LPT_W = nSLACK_vs_LPT_W+1}
    if (nSLACK == nLPT)     {nSLACK_vs_LPT_E = nSLACK_vs_LPT_E+1}
    if (nSLACK >  nLPT)     {nSLACK_vs_LPT_L = nSLACK_vs_LPT_L+1}
    #
    if (nSLACK <  nCOMBINE) {nSLACK_vs_COMBINE_W = nSLACK_vs_COMBINE_W+1}
    if (nSLACK == nCOMBINE) {nSLACK_vs_COMBINE_E = nSLACK_vs_COMBINE_E+1}
    if (nSLACK >  nCOMBINE) {nSLACK_vs_COMBINE_L = nSLACK_vs_COMBINE_L+1}
    #
    if (nSLACK <  nLDM)     {nSLACK_vs_LDM_W = nSLACK_vs_LDM_W+1}
    if (nSLACK == nLDM)     {nSLACK_vs_LDM_E = nSLACK_vs_LDM_E+1}
    if (nSLACK >  nLDM)     {nSLACK_vs_LDM_L = nSLACK_vs_LDM_L+1}

    #================================================
    # add the raw in dataframe mk_results
    #                          tm_results
    #================================================
    if (generateMethod_EnCours != ""|
        ab_Encours != ""|
        m_EnCours != 0) { 
      #----------------------------------------------------------------------
      # comparison Makespan part
      #----------------------------------------------------------------------
      mk_result_raw <-tibble(generateMethod=generateMethod_EnCours,'[a-b]'=ab_Encours, m=m_EnCours,
                          SLACK_vs_LPT_W    = nSLACK_vs_LPT_W,    SLACK_vs_LPT_E     = nSLACK_vs_LPT_E,    SLACK_vs_LPT_L    = nSLACK_vs_LPT_L,
                          SLACK_vs_COMBINE_W= nSLACK_vs_COMBINE_W,SLACK_vs_COMBINE_E = nSLACK_vs_COMBINE_E,SLACK_vs_COMBINE_L= nSLACK_vs_COMBINE_L,
                          SLACK_vs_LDM_W    = nSLACK_vs_LDM_W,    SLACK_vs_LDM_E     = nSLACK_vs_LDM_E,    SLACK_vs_LDM_L    = nSLACK_vs_LDM_L)
      #
      mk_results<-rbind(mk_results,mk_result_raw)  
      #----------------------------------------------------------------------
      # comparison Time part
      #----------------------------------------------------------------------
      tm_result_raw <-tibble(generateMethod=generateMethod_EnCours,'[a-b]'=ab_Encours, m=m_EnCours,
                             SLACK  = nTimeTot_SLACK, 
                             LPT    = nTimeTot_LPT, 
                             COMBINE=nTimeTot_COMBINE, 
                             LDM    =nTimeTot_LDM)
      #
      
      tm_results<-rbind(tm_results,tm_result_raw)
    } # if (generateMethod_EnCours != ""|
    
    #================================================
    # New raw (INIT)
    #================================================
    generateMethod_EnCours = ds$generateMethode[i]
    ab_Encours             = ds$`[a-b]`[i]
    m_EnCours              = ds$m[i]
    id_EnCours             = ds$id[i]

    #----------------------------------------------------------------------
    # comparison Makespan part
    #----------------------------------------------------------------------

    #---------------------------
    nSLACK_vs_LPT_W         = 0
    nSLACK_vs_LPT_E         = 0
    nSLACK_vs_LPT_L         = 0

    #---------------------------
    nSLACK_vs_COMBINE_W       = 0
    nSLACK_vs_COMBINE_E       = 0
    nSLACK_vs_COMBINE_L       = 0
    
    #---------------------------
    nSLACK_vs_LDM_W         = 0
    nSLACK_vs_LDM_E         = 0
    nSLACK_vs_LDM_L         = 0
    
    #---------------------------
    nLPT                    = 0
    nSLACK                  = 0
    nCOMBINE                = 0
    nLDM                    = 0
    
    #----------------------------------------------------------------------
    # comparison time part
    #----------------------------------------------------------------------

    #---------------------------
    nTimeTot_LPT            = 0
    nTimeTot_SLACK          = 0
    nTimeTot_COMBINE        = 0
    nTimeTot_LDM            = 0
  } # if (generateMethod_EnCours != ds$generateMethode[i]| ....

  ################################################################
  #
  #   RUPTURE id --> give results (who win ! for Makespan)
  #
  ################################################################
  if (id_EnCours != ds$id[i]){
    #
    if (nSLACK <  nLPT)     {nSLACK_vs_LPT_W = nSLACK_vs_LPT_W+1}
    if (nSLACK == nLPT)     {nSLACK_vs_LPT_E = nSLACK_vs_LPT_E+1}
    if (nSLACK >  nLPT)     {nSLACK_vs_LPT_L = nSLACK_vs_LPT_L+1}
    #
    if (nSLACK <  nCOMBINE) {nSLACK_vs_COMBINE_W = nSLACK_vs_COMBINE_W+1}
    if (nSLACK == nCOMBINE) {nSLACK_vs_COMBINE_E = nSLACK_vs_COMBINE_E+1}
    if (nSLACK >  nCOMBINE) {nSLACK_vs_COMBINE_L = nSLACK_vs_COMBINE_L+1}
    #
    if (nSLACK <  nLDM)     {nSLACK_vs_LDM_W = nSLACK_vs_LDM_W+1}
    if (nSLACK == nLDM)     {nSLACK_vs_LDM_E = nSLACK_vs_LDM_E+1}
    if (nSLACK >  nLDM)     {nSLACK_vs_LDM_L = nSLACK_vs_LDM_L+1}

    id_EnCours <- ds$id[i]
    #
    nLPT       = 0
    nSLACK     = 0
    nCOMBINE   = 0
    nLDM       = 0
  } # if (id_EnCours != ds$id[i]){
  
  ################################################################
  #
  #   MAIN CASE 
  #
  ################################################################
  #----------------------------------------------------------------------
  # comparison Makespan and time parts
  #----------------------------------------------------------------------

  #--------------------------- LPT
  if (ds$algoName[i] == "LPT")     {
    nLPT         = ds$makespan[i]
    nTimeTot_LPT = nTimeTot_LPT + ds$time[i]
  }
  
  #--------------------------- SLACK
  if (ds$algoName[i] == "SLACK")   {
    nSLACK     = ds$makespan[i]
    nTimeTot_SLACK = nTimeTot_SLACK + ds$time[i]
  }
  
  #--------------------------- COMBINE
  if (ds$algoName[i] == "COMBINE") {
    nCOMBINE = ds$makespan[i]
    nTimeTot_COMBINE = nTimeTot_COMBINE + ds$time[i]
  }
  
  #--------------------------- LDM
  if (ds$algoName[i] == "LDM")     {
    nLDM         = ds$makespan[i]
    nTimeTot_LDM = nTimeTot_LDM + ds$time[i]
  }
} # for (i in seq.int(nb_raws)){

#///////////////////////////////////////////////////////////////
# COMPUTE LAST BREAKING 
#///////////////////////////////////////////////////////////////

#================================================
# ID
#================================================
if (nSLACK <  nLPT)     {nSLACK_vs_LPT_W = nSLACK_vs_LPT_W+1}
if (nSLACK == nLPT)     {nSLACK_vs_LPT_E = nSLACK_vs_LPT_E+1}
if (nSLACK >  nLPT)     {nSLACK_vs_LPT_L = nSLACK_vs_LPT_L+1}
#
if (nSLACK <  nCOMBINE) {nSLACK_vs_COMBINE_W = nSLACK_vs_COMBINE_W+1}
if (nSLACK == nCOMBINE) {nSLACK_vs_COMBINE_E = nSLACK_vs_COMBINE_E+1}
if (nSLACK >  nCOMBINE) {nSLACK_vs_COMBINE_L = nSLACK_vs_COMBINE_L+1}
#
if (nSLACK <  nLDM)     {nSLACK_vs_LDM_W = nSLACK_vs_LDM_W+1}
if (nSLACK == nLDM)     {nSLACK_vs_LDM_E = nSLACK_vs_LDM_E+1}
if (nSLACK >  nLDM)     {nSLACK_vs_LDM_L = nSLACK_vs_LDM_L+1}

#----------------------------------------------------------------------
# comparison Makespan part
#----------------------------------------------------------------------
mk_result_raw <-tibble(generateMethod=generateMethod_EnCours,'[a-b]'=ab_Encours, m=m_EnCours,
                       SLACK_vs_LPT_W    = nSLACK_vs_LPT_W,    SLACK_vs_LPT_E     = nSLACK_vs_LPT_E,    SLACK_vs_LPT_L    = nSLACK_vs_LPT_L,
                       SLACK_vs_COMBINE_W= nSLACK_vs_COMBINE_W,SLACK_vs_COMBINE_E = nSLACK_vs_COMBINE_E,SLACK_vs_COMBINE_L= nSLACK_vs_COMBINE_L,
                       SLACK_vs_LDM_W    = nSLACK_vs_LDM_W,    SLACK_vs_LDM_E     = nSLACK_vs_LDM_E,    SLACK_vs_LDM_L    = nSLACK_vs_LDM_L)
#
mk_results<-rbind(mk_results,mk_result_raw)  
#----------------------------------------------------------------------
# comparison Time part
#----------------------------------------------------------------------
tm_result_raw <-tibble(generateMethod=generateMethod_EnCours,'[a-b]'=ab_Encours, m=m_EnCours,
                       SLACK  = nTimeTot_SLACK, 
                       LPT    = nTimeTot_LPT, 
                       COMBINE=nTimeTot_COMBINE, 
                       LDM    =nTimeTot_LDM)
tm_results<-rbind(tm_results,tm_result_raw)

#///////////////////////////////////////////////////////////////
#
#   RECORD RESULTS (MAKESPAN and TIMES)
#
#///////////////////////////////////////////////////////////////
write.table(mk_results, file = "dellaCroce_makesan.csv",
            sep = "\t", row.names = F)
write.table(tm_results, file = "dellaCroce_time.csv",
            sep = "\t", row.names = F)
