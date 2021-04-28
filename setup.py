#Homemade lib
import setup as s

#PYTHON lib
import time
import os
import json
# from subprocess import call
import subprocess


####################################################################
#
# CONSTANTS
#
####################################################################

#=========================================
# OS Name
# Values LINUX
#        WINDOWS
#=========================================
OS_NAME = "LINUX"

#=========================================
# folders
#=========================================
FOLDER_RESULTS   = "results"
FOLDER_ANALYSIS  = "analysis"
FOLDER_ZIPPEDLOG = "gz"
FOLDER_PWA       = "logpwa"

#=========================================
# PWA file catalog
#=========================================
URL_CATALOG_PWA = "https://www.cs.huji.ac.il/labs/parallel/workload/logs-list"

#=========================================
# to be exported with the result
#=========================================
EXP_INSTANCES = True
EXP_PARAMETERS = True

#=========================================
# generate integers rather than reals.
# arround with round method
# Used in MATRIX module __init__ method
# if True, generate a list of integers
#=========================================
INT_UNIFORM     = True
INT_NON_UNIFORM = True
# not relevant and therefore not managed.
# INT_LAMBDA      = False
# INT_BETA        = False
# INT_EXPONENTIAL = False
# INT_PWA = False

####################################################################
#
# TOOLS
#
#   sepDir  / or \ ?
#   folder  folder f exists ? create it if not. 
# 
####################################################################
def sepDir():
    """
    Directory separator
    return "/" if OS_NAME = "LINUX
    return "\" else
    """
    linuxPrefix = "/"
    winPrefix   = "\\"

    sep = linuxPrefix
    if OS_NAME != "LINUX":
        sep = winPrefix
    # END IF
    return sep
    
def folder(f):
    """
    Verify if folder f exists.
    if not create it
    return the folder prefixed with the relative path. eg ./f (for linux) or .\f (for windows)
    """
    # INIT
    currentPath = os.getcwd()
    # resFolder = "." + sepDir() + f
    resFolder = currentPath + sepDir() + f

    # Create folder if not exists
    if not os.path.exists(resFolder):
        os.makedirs(resFolder)
    # END IF
    return resFolder

def folderResult(name, user, date):
    folder(FOLDER_RESULTS)
    r = folder(FOLDER_RESULTS+ sepDir() + name+"_"+user+"_"+date)
    return r

def folderResultMatrix(name, user, date):
    folderReultCampaign = FOLDER_RESULTS+ sepDir() + name+"_"+user+"_"+date
    folder(FOLDER_RESULTS)
    folder(folderReultCampaign)
    r = folder(folderReultCampaign + sepDir()+"instanceFiles")
    return r

def campaignFileResultName(name=None, user=None, date=None):
    # return name+"_"+user+"_"+date
    return "result"

def campaignFileParametersName(name, user, date, ext = ".json"):
    return "parameters_" + name + "_" + user + "_" + date + ext

####################################################################
#
# running an R script
#
####################################################################
def analysisExecute(rFileName, workDir):
    currentDir = os.getcwd()
    output = None

    if OS_NAME == "LINUX":
        command_lin = ["Rscript", rFileName] # "--vanilla",
        print("####################")
        print("run >>"+rFileName)
        try:
            os.chdir(workDir)                                   # required to find the files (pdf) created by the R scripts
            output = subprocess.call(command_lin, shell=False)  # shell=False otherwise, do not execute the
            print("OK", output)
        except subprocess.CalledProcessError as e:
            chemin = os.getcwd() 
            output = e.output
            print("ERREUR", chemin, e)
        # END TRY
    else:
        # !!!! not tested !!!!
        os.chdir(workDir)                                   # required to find the files (pdf) created by the R scripts
        command_notLin = "cmd /k Rscript --vanilla < "+rFileName
        os.system(command_notLin)
    # END IF

    # retrieve current directory
    os.chdir(currentDir)

####################################################################
# CLASS ParamFile
# JSON Parameters files Management
#
####################################################################
class ParamFile:
    # ==================================================================
    # CONSTRUCTOR
    # ==================================================================
    def __init__(self):
        # JSON PARAMETERS FILE      
        self.campaignDate = time.strftime("%d%m%Y")
        # JSON content
        self.fileObj   = {} 

    # ==================================================================
    # CREATE
    # initialize values and JSON? content
    # save file
    # ==================================================================
    def create(self,
               campaignName, campaignUser,
               seedForce,
               N_NumberBegin,N_NumberEnd,N_List, M_NumberBegin,M_NumberEnd, M_List,
               matUniformNumber,matNonUniformNumber,matGammaNumber,matBetaNumber,matExponentialNumber,
               matRealFiles,
               A, B,
               Alpha,Beta,Lmbda,
               useLPT,useSLACK,useLDM,useCOMBINE,useMULTIFIT):
                               
        # JSON PARAMETERS FILE      
        self.campaignName = campaignName
        self.campaignUser = campaignUser

        # complete file name
        resDir = folderResult(self.campaignName, self.campaignUser, self.campaignDate)
        self.completeFileName = resDir + s.sepDir() + campaignFileParametersName(campaignName, campaignUser, self.campaignDate)

        # self.fileObj : json content
        #
        self.fileObj['campaign']=[]
        self.fileObj['campaign'].append({
            'campaignName'  : self.campaignName,
            'campaignUser'  : self.campaignUser,
            'campaignDate'  : self.campaignDate})
        #
        self.fileObj['size']=[]
        self.fileObj['size'].append({
            'N_NumberBegin' : N_NumberBegin,
            'N_NumberEnd'   : N_NumberEnd,
            'M_NumberBegin' : M_NumberBegin,
            'M_NumberEnd'   : M_NumberEnd,
            'N_List'        : N_List,
            'M_List'        : M_List})
        
        #
        self.fileObj['generation_methods']=[]
        self.fileObj['generation_methods'].append({
            'seedForce'            : seedForce,
            'matUniformNumber'     :matUniformNumber,
            'matNonUniformNumber'  :matNonUniformNumber,
            'matGammaNumber'       : matGammaNumber  ,
            'matBetaNumber'        : matBetaNumber,
            'matExponentialNumber' : matExponentialNumber})
        #
        self.fileObj['generation_PWA']=[]
        self.fileObj['generation_PWA'].append({
            'matRealFiles' : matRealFiles})
        #
        self.fileObj['generation_properties']=[]
        self.fileObj['generation_properties'].append({
            'A' : A,
            'B' : B,
            'Alpha' : Alpha,
            'Beta' : Beta,
            'Lambda' : Lmbda})
        #
        self.fileObj['algorithms'] = []
        self.fileObj['algorithms'].append({
            'useLPT' : useLPT,
            'useSLACK' : useSLACK,
            'useLDM' : useLDM,
            'useCOMBINE' : useCOMBINE,
            'useMULTIFIT' : useMULTIFIT,})
        # Save file
        self.save()

    # ==================================================================
    # READ File
    # open file
    # read values
    # return tuple 
    # ==================================================================
    def read(self,completeFileName):
        self.completeFileName = completeFileName
        with open(self.completeFileName) as jsonFile:
            dd = json.load(jsonFile)
        newDict = {}
        # read the json dict
        for val in dd.values():
            for i in range(len(val)):
                for param,value in val[i].items():
                    newDict[param]= value
                # END FOR
            # END FOR
        # END FOR
        return newDict
        
    # ==================================================================
    # SAVE
    # ==================================================================
    def save(self):
        with open(self.completeFileName,'w') as fileJSON:
            json.dump(self.fileObj, fileJSON)


####################################################################
#
# JSON INSTANCE files Management
#
####################################################################
class InstanceFile:
    # ==================================================================
    # CONSTRUCTOR
    # ==================================================================
    def __init__(self):
        # JSON PARAMETERS FILE      
        # JSON content
        self.fileObj   = {} 

    # ==================================================================
    # CREATE
    # initialize values and JSON? content
    # save file
    # ==================================================================
    def create(self,    campaignName, campaignUser, campaignDate,
                        generateMethode, seed, realFilesName, a, b, alpha,beta,lmbda, m, n, sType,
                        matTimes, 
                        lowBound, matStatIndicators, optimal = None):
                                       


        # complete file name
        resDir = folderResultMatrix(campaignName, campaignUser, campaignDate)
        print(resDir)
        self.completeFileName = resDir + s.sepDir() + "instance_"+sType+"_"+generateMethode+"_"+str(seed)+"_"+str(n)+"_"+str(m)+".json"
        print(self.completeFileName)
        
        # self.fileObj : json content
        #
        self.fileObj['campaign']=[]
        self.fileObj['campaign'].append({
            'campaignName'  : campaignName,
            'campaignUser'  : campaignUser,
            'campaignDate'  : campaignDate})
        #
        self.fileObj['generation_method']=[]
        self.fileObj['generation_method'].append({
            'generateMethode':generateMethode,
            'n'             : n,
            'm'             : m,
            'type'          : sType,
            'seed'          : seed,
            'reelFileName'  : realFilesName,
            'a'             : a,
            'b'             : b,
            'alpha'         : alpha,
            'beta'          : beta,
            'lambda'        : lmbda})
        #
        self.fileObj['features']=[]
        self.fileObj['features'].append({
            'lowBound'      : lowBound,
            'optimal'       : optimal,
            'indicators'    : matStatIndicators})
        #
        self.fileObj['matrix']=[]
        self.fileObj['matrix'].append({
            'timeList' : matTimes})
        # Save file
        self.save()

    # ==================================================================
    # SAVE
    # ==================================================================
    def save(self):
        with open(self.completeFileName,'w') as fileJSON:
            json.dump(self.fileObj, fileJSON)

    # ==================================================================
    # READ File
    # open file
    # read values
    # return tuple 
    # ==================================================================
    def read(self,completeFileName):
        self.completeFileName = completeFileName
        with open(self.completeFileName) as jsonFile:
            dd = json.load(jsonFile)
        newDict = {}
        # read the json dict
        for val in dd.values():
            for i in range(len(val)):
                for param,value in val[i].items():
                    newDict[param]= value
                # END FOR
            # END FOR
        # END FOR
        print(newDict)
        return newDict

