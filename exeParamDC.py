# homemade
import campaign          as cp
import matrix            as cm
import algorithms        as cmm
import ScheduleManagment as sm
import setup             as s  
import pwa               as pwa

def main():
    # #######################################################################
    #                                                                       #
    #                PARAMETERS TO BE MODIFIED                              #
    #                                                                       #
    #               Modify the desired values                               #
    #               save py file (ctrl+s)                                   #
    #               then press F5 to execute   (if idle is used)                             #
    #                                                                       #
    # #######################################################################

    #Campaign title and name ==============================================
    campNames_5 = ["dCroce_1_100_i50_m5_n10_50_100_500_1000",
                   "dCroce_1_1000_i50_m5_n10_50_100_500_1000",
                   "dCroce_1_10000_i50_m5_n10_50_100_500_1000"]
    campNames_x = ["dCroce_1_100_i40_m10_25_n50_100_500_1000",
                   "dCroce_1_1000_i40_m10_25_n50_100_500_1000",
                   "dCroce_1_10000_i40_m10_25_n50_100_500_1000"]
    bValues = [100, 1000, 10000]

    campaignUser         = "FCO"            # string

    # Seed ================================================================
    seedForce            = None             # integer
    # Job Set size with N_NumberEnd >= N_NumberBegin ======================
    N_NumberBegin        = 0               # int
    N_NumberEnd          = 0             # int
    # Machines number with M_NumberEnd >= M_NumberBegin ===================
    M_NumberBegin        = 1                # int
    M_NumberEnd          = 0               # int
    # Job set generation methods ===========================================
    matUniformNumber    = 10                # int
    matNonUniformNumber = 10                 # int 
    matGammaNumber      = 0                 # int
    matBetaNumber       = 0                 # int
    matExponentialNumber= 0                 # int
    # From Parallel WorkLoad Archive ======================================
    # pwa.pwaFileChoice(X) if None asc you witch file to use eg pwa.pwaFileChoice()
    #                       if 1   use all files present in the PWA folder
    #                       if 0   does not use any of the files present   
    matRealFiles        = pwa.pwaFileChoice(0)
    # Properties of generation ============================================
    nAlpah              = 1.0               # float for gamma (k) and beta (alpha)
    nBeta               = 1.0               # float for gamma (theta)
    nLambda             = 1.0               # float for exponential (lambda)
    #Algorithms ==========================================================
    useLPT              = 1                 # 1 or 0
    useSLACK            = 1                 # 1 or 0
    useLDM              = 1                 # 1 or 0
    useCOMBINE          = 1                 # 1 or 0
    useMULTIFIT         = 0                 # 1 or 0

    # #######################################################################
    #                                                                       #
    #                APPLICATION PART                                       #
    #                do not change anything here                            #
    #                                                                       #
    # #######################################################################
    print("===============================================================")
    print("Results computation                                            ")
    print("===============================================================")
    
    for camp in range(50):
        for b in range(3):
            
            #====================================================================
            # 1 - 100x
            #====================================================================
            nAb = 1.0   
            nBb = bValues[b] 

            #--------------------------------------------------------------------
            # i50 with 5 machines
            #--------------------------------------------------------------------
            campaignName = campNames_5[b]+str(camp)
            # LIST OF JOBS Numbers 
            N_List   = [10,50,100,500,1000]
            # LIST OF MACHINES Number 
            M_List   = [5]
        
            # Parameters file (json)
            if s.EXP_PARAMETERS:
                fileSetup = s.ParamFile()
                fileSetup.create(campaignName,campaignUser,
                                 seedForce,N_NumberBegin,N_NumberEnd,N_List, M_NumberBegin,M_NumberEnd, M_List,
                                 matUniformNumber,matNonUniformNumber,matGammaNumber,matBetaNumber,matExponentialNumber,
                                 matRealFiles,
                                 nAb, nBb,nAlpah,nBeta,nLambda,
                                 useLPT,useSLACK,useLDM,useCOMBINE,useMULTIFIT)
            # Create campaign
            c = cp.Campaign(campaignName, campaignUser,
                            N_NumberBegin, N_NumberEnd, N_List,
                            M_NumberBegin, M_NumberEnd, M_List,
                            matUniformNumber, matNonUniformNumber, matGammaNumber, matBetaNumber, matExponentialNumber, matRealFiles,
                            nAb, nBb, nAlpah, nBeta, nLambda, seedForce)
            # Apply algorithms
            if useLPT==1:      c.runAlgorithm(cmm.lpt)
            if useSLACK==1:    c.runAlgorithm(cmm.slack)
            if useLDM==1:      c.runAlgorithm(cmm.ldm)
            if useCOMBINE==1:  c.runAlgorithm(cmm.combine)
            if useMULTIFIT==1: c.runAlgorithm(cmm.multifit)
            c.exportCSV()

            #--------------------------------------------------------------------
            # i40 with 10, 25 machines
            #--------------------------------------------------------------------
            campaignName = campNames_x[b]+str(camp)
            # LIST OF JOBS Numbers 
            N_List   = [50,100,500,1000]
            # LIST OF MACHINES Number 
            M_List   = [10,25]
            # Parameters file (json)
            if s.EXP_PARAMETERS:
                fileSetup = s.ParamFile()
                fileSetup.create(campaignName,campaignUser,
                                 seedForce,N_NumberBegin,N_NumberEnd,N_List, M_NumberBegin,M_NumberEnd, M_List,
                                 matUniformNumber,matNonUniformNumber,matGammaNumber,matBetaNumber,matExponentialNumber,
                                 matRealFiles,
                                 nAb, nBb,nAlpah,nBeta,nLambda,
                                 useLPT,useSLACK,useLDM,useCOMBINE,useMULTIFIT)
            # Create campaign
            c = cp.Campaign(campaignName, campaignUser,
                            N_NumberBegin, N_NumberEnd, N_List,
                            M_NumberBegin, M_NumberEnd, M_List,
                            matUniformNumber, matNonUniformNumber, matGammaNumber, matBetaNumber, matExponentialNumber, matRealFiles,
                            nAb, nBb, nAlpah, nBeta, nLambda, seedForce)
            # Apply algorithms
            if useLPT==1:      c.runAlgorithm(cmm.lpt)
            if useSLACK==1:    c.runAlgorithm(cmm.slack)
            if useLDM==1:      c.runAlgorithm(cmm.ldm)
            if useCOMBINE==1:  c.runAlgorithm(cmm.combine)
            if useMULTIFIT==1: c.runAlgorithm(cmm.multifit)
            c.exportCSV()
        # END FOR
    # END FOR
if __name__ == "__main__":
    main()
