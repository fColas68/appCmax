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
    #               then press F5 to execute                                #
    #                                                                       #
    # #######################################################################

    #Campaign title and name ==============================================
    campaignName         = "testParam4"     # string
    campaignUser         = "FCO"            # string

    # Seed ================================================================
    seedForce            = None             # integer

    # Job Set size with N_NumberEnd >= N_NumberBegin ======================
    N_NumberBegin        = 50               # int
    N_NumberEnd          = 100               # int 

    # Machines number with M_NumberEnd >= M_NumberBegin ===================
    M_NumberBegin        = 4                # int
    M_NumberEnd          = 4                # int

    # Job set generation methods ===========================================
    matUniformNumber    = 0                 # int
    matNonUniformNumber = 0                 # int 
    matGammaNumber      = 1                 # int
    matBetaNumber       = 0                 # int
    matExponentialNumber= 0                 # int

    # From Parallel WorkLoad Archive ======================================
    # pwa.pwaFileChoice(X) if None asc you witch file to use eg pwa.pwaFileChoice()
    #                       if 1   use all files present in the PWA folder
    #                       if 0   does not use any of the files present   
    matRealFiles        = pwa.pwaFileChoice(0)

    # Properties of generation ============================================
    nAb                 = 1.0               # float
    nBb                 = 100.0             # float
    nAlpah              = 1.0               # float
    nBeta               = 1.0               # float
    nLambda             = 1.0               # float

      #Algorithms ==========================================================
    useLPT              = 1                 # 1 or 0
    useSLACK            = 1                 # 1 or 0
    useLDM              = 1                 # 1 or 0
    useCOMBINE          = 0                 # 1 or 0
    useMULTIFIT         = 0                 # 1 or 0

    # #######################################################################
    #                                                                       #
    #                APPLICATION PART                                       #
    #                do not change anything here                            #
    #                                                                       #
    # #######################################################################

    #======================================================================
    # Parameters file (json)
    #======================================================================
    fileSetup = s.ParamFile()
    fileSetup.create(campaignName,campaignUser,
                     seedForce,N_NumberBegin,N_NumberEnd,M_NumberBegin,M_NumberEnd,
                     matUniformNumber,matNonUniformNumber,matGammaNumber,matBetaNumber,matExponentialNumber,
                     matRealFiles,
                     nAb, nBb,nAlpah,nBeta,nLambda,
                     useLPT,useSLACK,useLDM,useCOMBINE,useMULTIFIT)
    print("===============================================================")
    print("Results computation                                            ")
    print("===============================================================")
    c = cp.Campaign(campaignName, campaignUser, N_NumberBegin, N_NumberEnd, M_NumberBegin, M_NumberEnd, matUniformNumber, matNonUniformNumber, matGammaNumber, matBetaNumber, matExponentialNumber, matRealFiles, nAb, nBb, nAlpah, nBeta, nLambda, seedForce)
    #
    if useLPT==1: c.runAlgorithm(cmm.lpt)
    if useSLACK==1: c.runAlgorithm(cmm.slack)
    if useLDM==1: c.runAlgorithm(cmm.ldm)
    if useCOMBINE==1: c.runAlgorithm(cmm.combine)
    if useMULTIFIT==1: c.runAlgorithm(cmm.multifit)
    c.exportCSV()

if __name__ == "__main__":
    main()
