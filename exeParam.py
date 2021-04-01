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
    campaignName         = "testParam2"      # string
    campaignUser         = "FCO"            # string

    # Seed ================================================================
    seedForce            = None             # integer

    # Job Set size with N_NumberEnd >= N_NumberBegin ======================
    N_NumberBegin        = 10               # int
    N_NumberEnd          = 40               # int 

    # Machines number with M_NumberEnd >= M_NumberBegin ===================
    M_NumberBegin        = 3                # int
    M_NumberEnd          = 3                # int

    # Job set generation methods ===========================================
    matUniformNumber    = 1                 # int
    matNonUniformNumber = 0                 # int 
    matGammaNumber      = 0                 # int
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
    useCOMBINE          = 1                 # 1 or 0





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
                     useLPT,useSLACK,useLDM,useCOMBINE)
    print("===============================================================")
    print("Results computation                                            ")
    print("===============================================================")
    c = cp.Campaign(campaignName, campaignUser, N_NumberBegin, N_NumberEnd, M_NumberBegin, M_NumberEnd, matUniformNumber, matNonUniformNumber, matGammaNumber, matBetaNumber, matExponentialNumber, matRealFiles, nAb, nBb, nAlpah, nBeta, nLambda, seedForce)
    #
    if useLPT==1: c.runAlgorithm(cmm.lpt)
    if useSLACK==1: c.runAlgorithm(cmm.slack)
    if useLDM==1: c.runAlgorithm(cmm.ldm)
    if useCOMBINE==1: c.runAlgorithm(cmm.combine)
    c.exportCSV()

if __name__ == "__main__":
    main()
