import time
import pandas as pd     
import os               # to use path 
import shutil           # copy files

import matrix            as cm
import algorithms        as cmm
import ScheduleManagment as sm
import pwa               as pwa
import setup             as s

class Campaign():

    # #######################################################################
    # CONSTRUCTOR
    # #######################################################################
    def __init__(self, campaignName, campaignUser, N_NumberBegin, N_NumberEnd, N_List, M_NumberBegin, M_NumberEnd, M_List, matUniformNumber, matNonUniformNumber, matGammaNumber, matBetaNumber, matExponentialNumber, matRealFiles, a, b, alpha, beta, lambd, seedForce = None):
        # set of testing matricies -------------------------------------
        self.matricies           = []
        #---------------------------------------------------------------
        self.campaignName        = campaignName
        self.campaignDate        = time.strftime("%d%m%Y")  
        self.campaignUser        = campaignUser
        self.compainCompleteName = s.campaignFileResultName(self.campaignName,self.campaignUser,self.campaignDate)
        #---------------------------------------------------------------
        self.N_NumberBegin        = N_NumberBegin
        self.N_NumberEnd          = N_NumberEnd
        self.N_List               = N_List
        self.M_NumberBegin        = M_NumberBegin
        self.M_NumberEnd          = M_NumberEnd
        self.M_List               = M_List
        #---------------------------------------------------------------
        self.matUniformNumber    = matUniformNumber
        self.matNonUniformNumber = matNonUniformNumber
        self.matGammaNumber      = matGammaNumber
        self.matBetaNumber       = matBetaNumber
        self.matExponentialNumber= matExponentialNumber
        #---------------------------------------------------------------
        self.matRealFiles        = matRealFiles[:]
        #---------------------------------------------------------------
        self.a                   = a
        self.b                   = b
        self.alpha               = alpha
        self.beta                = beta
        self.lambd               = lambd
        #---------------------------------------------------------------
        self.seed = None #essential 
        if seedForce:
            self.seed            = seedForce
        # END IF    
            
        # CREATE "SET OF TIMES INSTANCIES" IN self.matricies
        self.createMatricies()

    # #######################################################################
    # MATRICIES CONSTRUCTION
    # #######################################################################
    def createMatricies(self):
        #=====================================================
        # filling in the iteration lists.
        # Jobs N_List and Machines M_List
        #=====================================================
        # j job iterator
        if len(self.N_List) == 0:
            for j in range(self.N_NumberBegin, self.N_NumberEnd+1):
                self.N_List.append(j)
        # END IF
        # i machines iterator
        if len(self.M_List) == 0:
            for i in range(self.M_NumberBegin, self.M_NumberEnd+1):
                self.M_List.append(i)
        # END IF
        #=====================================================
        # according statistics distributions
        # j is the jobs iterator
        # i is the machines itérator
        #=====================================================
        for j in range(len(self.N_List)):
            for i in range(len(self.M_List)):
                # UNIFORM 
                for k in range(self.matUniformNumber):
                    m = cm.PTimes("UNIFORM", self.N_List[j], self.M_List[i], self.a, self.b, self.alpha, self.beta, self.lambd, "", self.seed)
                    self.matricies.append(m)
                # END FOR    

                # NON UNIFORM P    
                for k in range(self.matNonUniformNumber):
                    m = cm.PTimes("NON_UNIFORM", self.N_List[j], self.M_List[i], self.a, self.b, self.alpha, self.beta, self.lambd, "", self.seed)
                    self.matricies.append(m)
                # END FOR
                
                # GAMMA P    
                for k in range(self.matGammaNumber):
                    m = cm.PTimes("GAMMA", self.N_List[j], self.M_List[i], self.a, self.b, self.alpha, self.beta, self.lambd, "", self.seed)
                    self.matricies.append(m)
                # END FOR
                
                # BETA P    
                for k in range(self.matBetaNumber):
                    m = cm.PTimes("BETA", self.N_List[j], self.M_List[i], self.a, self.b, self.alpha, self.beta, self.lambd, "", self.seed)
                    self.matricies.append(m)
                # END FOR

                # EXPENENTIAL P    
                for k in range(self.matExponentialNumber):
                    m = cm.PTimes("EXPONENTIAL", self.N_List[j], self.M_List[i], self.a, self.b, self.alpha, self.beta, self.lambd, "", self.seed)
                    self.matricies.append(m)
                # END FOR
            # END for i in range(self.M_NumberBegin, self.M_NumberEnd)):
        # END FOR for i in range(self.N_NumberBegin, self.N_NumberEnd):

        #=====================================================
        # Real life jobs log
        # i is the machines itérator
        #=====================================================
        for i in range(len(self.M_List)):
            # REAL P    
            for k in range(len(self.matRealFiles)):
                m = cm.PTimes("REAL", None, self.M_List[i], None, None, None, None, None, self.matRealFiles[k])
                # m = cm.PTimes("REAL", j, i, self.a, self.b, self.alpha, self.beta, self.lambd, self.matRealFiles[k])
                self.matricies.append(m)
            # END FOR    
        # END for i in range(self.M_NumberBegin, self.M_NumberEnd)):

    # #######################################################################
    # RUN ALGORITHMS
    # #######################################################################
    def runAlgorithm(self, algo):
        """
        algo is a function from algorithm.py
        lpt
        slack
        combine
        ldm
        ...
        """
        # each matricies[k] is a PTimes object
        for k in range(len(self.matricies)):
            # work with PTimes.Times list cmm.lpt
            r = algo(self.matricies[k].Times, self.matricies[k].m)
            self.matricies[k].addSched(r)
            print("best result      :",self.matricies[k].BestResult_Makespan,", Obtained :",r.getMakespan(), ", Time:", r.getTime())
            
            # work with PTimes.m1Times list
            rm1 = algo(self.matricies[k].m1Times, self.matricies[k].m)
            print(rm1)
            self.matricies[k].addM1Sched(rm1)
            print("Expected optimal :",self.matricies[k].m1Optimal,", Obtained :",rm1.getMakespan(), ", Time:", rm1.getTime())
        # END FOR    

    # #######################################################################
    # CSV EXPORT
    # #######################################################################
    def exportCSV(self):
        
        #====================================================================
        #
        #               EXPORT RESULT VIA DATA FRAME
        #
        #====================================================================

        #------------------------------------        
        # target file 
        # ...../result/campaignname_user_date/ file.csv
        #------------------------------------        
        resDir = s.folderResult(self.campaignName, self.campaignUser, self.campaignDate)
        filenameResult = resDir + s.sepDir()+ self.compainCompleteName+".csv"

        #------------------------------------
        # chck for user
        #------------------------------------        
        print("Exporting campaign result to %s . please wait..." % (filenameResult))
        #
        # collumns = ""
        dataResult       = []
        #print(len(self.matricies))

        #------------------------------------        
        # one row per matrice instance and per algorithm.
        # one time for native instance
        # one time for completed m-1 instance
        #------------------------------------        
        for k in range(len(self.matricies)):
            
            # matricies[k] is a PTimes object
            items = self.matricies[k].getResultForCSV()
            for i in range(len(items)):
                dataResult.append(items[i])
            # END FOR (for i in range(len(items)):)
            
        # END FOR (for k in range(len(self.matricies)):)

        #------------------------------------        
        # EXPORT
        #------------------------------------        
        expResultHeader = cm.PTimes.getResultForCSVHeader()
        expResult = pd.DataFrame(dataResult) #, collumns)
        expResult.to_csv(filenameResult, index=False, header=expResultHeader)

        #====================================================================
        #
        #                   EXPORT matricies (Time lists)
        #
        #====================================================================

        if s.EXP_INSTANCES:
            for k in range(len(self.matricies)):
                # matricies[k] is a PTimes object
                items = self.matricies[k]
                #------------------------------------        
                # native matrix part (json InstanceFile)
                #------------------------------------        
                instanceFileNative = s.InstanceFile()
                instanceFileNative.create(self.campaignName, self.campaignUser, self.campaignDate,
                                          items.generateMethode, items.seed, items.fileName, items.a, items.b, items.alpha,items.beta,items.lambd, items.m, items.n, "NATIVE",
                                          items.Times, 
                                          items.LowBound, items.StatIndicators)
            
                #------------------------------------        
                # completed with m-1 jobs matrix part (json InstanceFile)
                #------------------------------------        
                instanceFileNative = s.InstanceFile()
                instanceFileNative.create(self.campaignName, self.campaignUser, self.campaignDate,
                                          items.generateMethode, items.seed, items.fileName, items.a, items.b, items.alpha,items.beta,items.lambd, items.m, items.m1_n, "COMPLETEDM1",
                                          items.m1Times, 
                                          items.m1LowBound, items.m1StatIndicators, items.m1Optimal)
            # END FOR
        # END IF if s.EXP_INSTANCES:

        #====================================================================
        #
        #           COPY ANALYSIS SCRIPTS FROM AALYSIS TO RESULTS FOLDER
        #       and EXECUTE THEME
        #
        #====================================================================
        a = s.folder(s.FOLDER_ANALYSIS)
        content = os.listdir(a)
        for fileName in content:
            if fileName.endswith(".r"):

                # copy
                filePath = shutil.copy(a+s.sepDir()+fileName, resDir)

                # execute
                s.analysisExecute(resDir+s.sepDir()+fileName)

            # END IF
        # END FOR

        

        #====================================================================
        #
        #         COPY ANALYSIS SCRIPTS FROM AALYSIS TO RESULTS FOLDER
        #
        #====================================================================

        

        #------------------------------------
        # check for user
        #------------------------------------        
        print("Done !")
