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
    #                PARAMETERS TO BE MODIFIED                              #
    #                                                                       #
    #               Modify the desired values                               #
    #               save py file (ctrl+s)                                   #
    #               then press F5 to execute                                #
    #                                                                       #
    # #######################################################################

    #Campaign title and name ==============================================
    campaignName         = "dCroce_1_10000_50_10-50-100-500-1000"   # string
    campaignUser         = "FCO"            # string
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

    root = tk.Tk()
    root.withdraw()                 # pour ne pas afficher la fenêtre Tk
    name = askopenfilename(initialdir=s.folder(s.FOLDER_RESULTS), filetypes=[("json instance files","*.json")])
    if not name: return
    ifile = s.InstanceFile()
    d = ifile.read(name) # D is a dictionnary with keys parameters

    print("===============================================================")
    print("Retrieve instance informations")
    print("===============================================================")

    #Campaign title and name ==============================================
    campaignName         = d["campaignName"]
    campaignUser         = d["campaignUser"]
    campaignDate         = d["campaignDate"]

    # Generation ==========================================================
    seed                 = d["seed"]
    genrationMethod      = d["generateMethode"]
    a                    = d["a"]
    b                    = d["b"]
    alpha                = d["alpha"]
    beta                 = d["beta"]
    lambd                = d["lambda"]
    pwafileName          = d["reelFileName"]
    
    # properties ==========================================================
    genType              = d["type"]
    n                    = d["n"]
    m                    = d["m"]
    indicators           = d["indicators"]

    # Time List ==========================================================
    timeList             = d["timeList"]

    # Alogrithm  result ==================================================
    result =  []
    
    print("Campaign ================")
    print("Date . . . . . . . . . : ",campaignDate)
    print("User . . . . . . . . . : ",campaignUser)
    print("Name . . . . . . . . . : ",campaignDate)

    print("Generation =============")
    print("Seed  . . . . . . . .  : ", seed)
    print("Method. . . . . . . .  : ", genrationMethod)
    print("a . . . . . . . . . .  : ", a)
    print("b . . . . . . . . . .  : ", b)
    print("alpĥa . . . . . . . .  : ", alpha)
    print("beta. . . . . . . . .  : ", beta)
    print("lambda. . . . . . . .  : ", lambd)
    print("pwa file name . . . .  : ", pwafileName)

    print("Properties ============")
    print("type native/completed  : ", genType)
    print("n : time jobs number   : ",n)
    print("m : machines  number   : ",m)

    print("Time List ============")
    print(timeList)

    pRes = cmm.combine(timeList, m, verbose=True) # pRes is a (ScheduleManagment) sm.PSched
    pRes.printResult()
    
    


    
##    c = cp.Campaign(campaignName, campaignUser, N_NumberBegin, N_NumberEnd, N_List, M_NumberBegin, M_NumberEnd, M_List, matUniformNumber, matNonUniformNumber, matGammaNumber, matBetaNumber, matExponentialNumber, matRealFiles, nAb, nBb, nAlpah, nBeta, nLambda, seedForce)
##    #
##    if useLPT==1: c.runAlgorithm(cmm.lpt)
##    if useSLACK==1: c.runAlgorithm(cmm.slack)
##    if useLDM==1: c.runAlgorithm(cmm.ldm)
##    if useCOMBINE==1: c.runAlgorithm(cmm.combine)
##    if useMULTIFIT==1: c.runAlgorithm(cmm.multifit)
##    
##    c.exportCSV()

if __name__ == "__main__":
    main()
