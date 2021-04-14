#Homemade lib
import setup as s

#PYTHON lib
import time
import os
import json

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
OS_Name = "LINUX"

#=========================================
# folders
#=========================================
FOLDER_RESULTS   = "results"
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
    return "/" if OS_Name = "LINUX
    return "\" else
    """
    linuxPrefix = "/"
    winPrefix   = "\\"

    sep = linuxPrefix
    if OS_Name != "LINUX":
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
    resFolder = "." + sepDir() + f

    # Create folder if not exists
    if not os.path.exists(resFolder):
        os.makedirs(resFolder)
    # END IF
    return resFolder

def folderResult(name, user, date):
    folder(FOLDER_RESULTS)
    r = folder(FOLDER_RESULTS+ sepDir() + name+"_"+user+"_"+date)
    return r

def campaignFileResultName(name, user, date):
    return name+"_"+user+"_"+date

def campaignFileParametersName(name, user, date):
    return campaignFileResultName(name, user, date)+"_Param"

####################################################################
#
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
               N_NumberBegin,N_NumberEnd,M_NumberBegin,M_NumberEnd,
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
        self.completeFileName = resDir + s.sepDir() + campaignFileParametersName(campaignName, campaignUser, self.campaignDate)+".json"
        # self.fileObj : json content
        #
        self.fileObj['campaign']=[]
        self.fileObj['campaign'].append({
            'campaignName' : self.campaignName,
            'campaignUser' : self.campaignUser,
            'campaignDate' : self.campaignDate})
        #
        self.fileObj['size']=[]
        self.fileObj['size'].append({
            'N_NumberBegin' : N_NumberBegin,
            'N_NumberEnd' : N_NumberEnd,
            'M_NumberBegin' : M_NumberBegin,
            'M_NumberEnd' : M_NumberEnd})
        #
        self.fileObj['generation_methods']=[]
        self.fileObj['generation_methods'].append({
            'seedForce' : seedForce,
            'matUniformNumber' :matUniformNumber,
            'matNonUniformNumber' :matNonUniformNumber,
            'matGammaNumber' : matGammaNumber  ,
            'matBetaNumber': matBetaNumber,
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
                                       
        # JSON PARAMETERS FILE      

        # complete file name
        resDir = folderResult(campaignName, campaignUser, campaignDate)
        self.completeFileName = resDir + s.sepDir() + "instance_"+sType+"_"+generateMethode+"_"+str(seed)+"_"+str(n)+"_"+str(m)+".json"
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
