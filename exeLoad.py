# homemade
import campaign          as cp
import matrix            as cm
import algorithms        as cmm
import ScheduleManagment as sm
import setup             as s  
import pwa               as pwa
# Python
import tkinter as tk
from tkinter.filedialog import askopenfilename

def main():
    # #######################################################################
    #                                                                       #
    # #######################################################################
    
    root = tk.Tk()
    root.withdraw()                 # pour ne pas afficher la fenêtre Tk
    name = askopenfilename(initialdir=s.folder(s.FOLDER_RESULTS), filetypes=[("json parameters files","*.json")])
    if not name: return
    param = s.ParamFile()
    d = param.read(name) # D is a dictionnary with keys parameters

    #Campaign title and name ==============================================
    campaignName         = d["campaignName"]+"_reloaded"
    campaignUser         = d["campaignUser"]

    # Seed ================================================================
    seedForce            = d["seedForce"]

    # Job Set size with N_NumberEnd >= N_NumberBegin ======================
    N_NumberBegin        = d["N_NumberBegin"]
    N_NumberEnd          = d["N_NumberEnd"]
    N_List               = d["N_List"]

    # Machines number with M_NumberEnd >= M_NumberBegin ===================
    M_NumberBegin        = d["M_NumberBegin"]
    M_NumberEnd          = d["M_NumberEnd"]
    M_List               = d["M_List"]

    # Job set generation methods ===========================================
    matUniformNumber    = d["matUniformNumber"]
    matNonUniformNumber = d["matNonUniformNumber"]
    matGammaNumber      = d["matGammaNumber"]
    matBetaNumber       = d["matBetaNumber"]
    matExponentialNumber= d["matExponentialNumber"]

    # From Parallel WorkLoad Archive ======================================
    # pwa.pwaFileChoice(X) if None asc you witch file to use eg pwa.pwaFileChoice()
    #                       if 1   use all files present in the PWA folder
    #                       if 0   does not use any of the files present   
    matRealFiles        = d["matRealFiles"]

    # Properties of generation ============================================
    nAb                 = d["A"]
    nBb                 = d["B"]
    nAlpah              = d["Alpha"]
    nBeta               = d["Beta"]
    nLambda             = d["Lambda"]

    #Algorithms ==========================================================
    useLPT              = d["useLPT"]
    useSLACK            = d["useSLACK"]
    useLDM              = d["useLDM"]
    useCOMBINE          = d["useCOMBINE"]
    useMULTIFIT         = d["useMULTIFIT"]

    # #######################################################################
    #                                                                       #
    #                APPLICATION PART                                       #
    #                do not change anything here                            #
    #                                                                       #
    # #######################################################################

    #======================================================================
    # Parameters file (json)
    #======================================================================
    if s.EXP_PARAMETERS:
        fileSetup = s.ParamFile()
        fileSetup.create(campaignName,campaignUser,
                         seedForce,N_NumberBegin,N_NumberEnd, N_List, M_NumberBegin,M_NumberEnd, M_List, 
                         matUniformNumber,matNonUniformNumber,matGammaNumber,matBetaNumber,matExponentialNumber,
                         matRealFiles,
                         nAb, nBb,nAlpah,nBeta,nLambda,
                         useLPT,useSLACK,useLDM,useCOMBINE,useMULTIFIT)
    # END IF    

    print("===============================================================")
    print("Results computation                                            ")
    print("===============================================================")
    c = cp.Campaign(campaignName, campaignUser, N_NumberBegin, N_NumberEnd, N_List, M_NumberBegin, M_NumberEnd, M_List, matUniformNumber, matNonUniformNumber, matGammaNumber, matBetaNumber, matExponentialNumber, matRealFiles, nAb, nBb, nAlpah, nBeta, nLambda, seedForce)
    #
    if useLPT==1: c.runAlgorithm(cmm.lpt)
    if useSLACK==1: c.runAlgorithm(cmm.slack)
    if useLDM==1: c.runAlgorithm(cmm.ldm)
    if useCOMBINE==1: c.runAlgorithm(cmm.combine)
    if useMULTIFIT==1: c.runAlgorithm(cmm.multifit)
    #
    c.exportCSV()

if __name__ == "__main__":
    main()
