import time
from operator import attrgetter

# ########################################################################
#
#                               Processor
#
# part of schedule (Processor = machine)
# ########################################################################
class Processor:
    # =============================================
    # CONSTRUCTOR
    # =============================================
    def __init__(self):
        """
        :Param jobsTotal  :float = 0.0     # Stores the total time of the jobs loaded in the list.
        :param jobsGap    :float = 0.0     # stores the time span between the first and last job loaded in the list.
        :param jobsSet    :list  = []      # Stores jobs
        """
        self.jobsTotal  = 0.0
        self.jobsGap    = 0.0
        self.jobsSet    = []
    # =============================================
    # addJOB
    # =============================================
    def addJob(self, jobTime):
        """
        Add jobTime to the list self.jobsSet
        compute gap between max job and min job
        compute total jobs time
        """
        m = self.jobsSet[:]  # add item in the list
        m.append(jobTime)    # self.jobsSet.append(jobTime)        
        self.jobsSet = m[:]  # ---------------------
        #
        self.getTotal()      # total <=> self.jobsLoaded+=jobTime
        self.getGap()        # gap for slack <=> self.jobsSet[0]-jobTime

    # =============================================
    # Get
    # =============================================
    def getGap(self):
        self.jobsGap = max(self.jobsSet)-min(self.jobsSet)
        return self.jobsGap

    def getTotal(self):
        self.jobsTotal = sum(self.jobsSet)
        return self.jobsTotal

    def getJobsSetSize(self):
        return len(self.jobsSet)

    def getJobTime(self, k):
        return self.jobsSet[k]
    
    def razJobsSet(self):
        """
        raz object instance values
        """
        self.jobsTotal  = 0.0
        self.jobsGap    = 0.0
        self.jobsSet    = []

# ########################################################################
#
#                               ldmTuple
#
# list of pocessors
# ########################################################################
class ldmTuple:
    # =============================================
    # CONSTRUCTOR
    # =============================================
    def __init__(self, m):
        """        
        like ldm rule, Create a m-tuple with empty items
        e.g m = 5 [[],[],[],[],[]]
        each item is a Processor object

        :param tupl      : list  = []  as defined in the ldm algorithm. List of m Processors objects
        :param m         : int   = 0   number of machines(=procesors)
        :param tuplTotal : float = 0.0 stores the total time stored in each processor.
        :param tuplGap   : float = 0.0 stores the difference between the least loaded processor and the most loaded processor.
                                       Allows tuples to be sorted by this value, as described in the LDM algorithm.
        """
        self.m          = m
        self.tuplTotal  = 0.0
        self.tuplGap    = 0.0
        self.tupl       = [] # list of m Processor
        for i in range(m):
            p = Processor()
            self.tupl.append(p)

    # =============================================
    # initialization of ldm tuple
    # =============================================
    def initialize(self, value):
        """
        Affect the value to the last item of the ldmTuple, like LDM rule, 
        e.g for m = 3 and value = 2 then tupl = [ processor1.jobsSet=[], processor2.jobsSet=[], processor3.jobsSet=[2] ]
        compute (and stores) tuplTotal
        compute (and stores) tuplGap
        """
        self.tupl[self.m - 1].addJob(value)
        self.getTotal()
        self.getGap()
        
    # =============================================
    # GET
    # =============================================
    def getTotal(self):
        total = 0.0
        for i in range(len(self.tupl)):
            total+= sum(self.tupl[i].jobsSet)
        # END FOR
        self.tuplTotal = total
        #
        return self.tuplTotal
        
    def getGap(self):
        minmax = []
        gap = 0.0
        for i in range(len(self.tupl)):
            minmax.append(sum(self.tupl[i].jobsSet))
        # END FOR
        gap = max(minmax) - min(minmax)
        #
        self.tuplGap = gap
        #
        return self.tuplGap
    # =============================================
    # smaler (index of smaler loaded Processor)
    # =============================================
    def smaler(self):
        """
        return the index in the list tupl so the processor has the smallest sum.
        in the case of a tie, the index of the furthest right.
        """
        res = 0
        smalValue = None
        for k in range(len(self.tupl)):
            value = self.getProcessor(k).getTotal()
            if smalValue==None:
                smalValue = value
                res = k
            else:
                if value <= smalValue:
                    smalValue = value
                    res = k
                # END IF
            # END IF
        # END FOR
        return res
    # =============================================
    # largest (index of largest loaded Processor)
    # =============================================
    def largest(self):
        """
        return the index in the list tupl so the processor has the largest sum.
        in the case of a tie, the index of the furthest right.
        """
        res = 0
        largValue = 0
        for k in range(len(self.tupl)):
            value = self.getProcessor(k).getTotal()
            if value >= largValue:
                largValue = value
                res = k
            # END IF
        # END FOR
        return res

    # =============================================
    # getProcessor 
    # =============================================
    def getProcessor(self, m):
        """
        return Processor object from tuple index m
        """
        return self.tupl[m]
    

# ########################################################################
#
#                               ldmPartition
#
# list of ldmTuple
# ########################################################################
class ldmPartition():
    # =============================================
    # CONSTRUCTOR
    # =============================================
    def __init__(self, times, m):
        """
        Store in self.part (list) n ldmTuple
        each ldmTuple is an Object with tuplTotal tuplGap computed and ldmTuple.tupl (list ) filled with m Processors
        :param times (--> part) : list (see below)
        :param m                : int = 0 number of machines
        
        part ==> ldmTuple1                   - ldmTuple2 - ... - ldmTuple1n
                 -------------------           ---------         -------------------
                 ldmTuple1.tuplTotal           ...               ldmTuplen.tuplTotal
                 ldmTuple1.tuplGap             ...               ldmTuplen.tuplGap
                 ldmTuple1.tupl                                  ldmTuplen.tupl
                            ---------------                                ---------------
                            tupl.Processor1                                tupl.Processor1
                            tupl.Processor2                                tupl.Processor2
                            ...                                            ...
                            tupl.Processorm                                tupl.Processorm
        """
        self.m = m
        self.part = []
        n = len(times)
        # create part (list) of n ldmTuple (lists) of m Processor
        for i in range(n):
            t = ldmTuple(m)
            t.initialize(times[i])
            self.part.append(t)

    # =============================================
    # getPartSize
    # =============================================
    def getPartSize(self):
        return len(self.part)

    # =============================================
    # getSched
    # =============================================
    def getSched(self):
        if len(self.part) == 1:
            l = self.part[0].tupl[:]
            return l
        else:
            return []
        # END IF

    # =============================================
    # partSortBytuplGapDec
    # =============================================
    def partSortBytuplGapDec(self):
        """
        Sort part by non increasing part. ldmTupleX.tuplGap
        so as to obtain the m-tuples that have the largest difference (ldmTupleX.tuplGap) first.
        """
        self.part.sort(key=attrgetter("tuplGap"), reverse=True)

    # =============================================
    # partPrint
    # =============================================
    def partPrint(self):
        """
        Just for debug or verify result
        Print the part state represented by
        ldmTuple1 [][][][][]
        ldmTuple2 [][][][][]
        ...
        ldmTuplen [][][][][]
        each [] is the jobsSet of Processor objext
        """
        print("")
        print("partition size :",len(self.part))
        for i in range(len(self.part)):
            print("")
            for j in range(len(self.part[i].tupl)):
                print(self.part[i].tupl[j].jobsSet, end = " ")
    # =============================================
    # partMerge
    # =============================================
    def partMerge(self, tupl1Indice, tupl2Indice):
        """
        of two m-tuples, only one remains, by combining 
        the processor with the smaller sum of one with the larger sum of the other, and so on.
        e.g
        
        ldmTuple1 [3,3][4][4] gap=2 : (3+3) - 4
        ldmTuple2 [][][][1]   gap=1 : 1-0
        ...
        ldmTuplen [][][][][]
        result
        ldmTuple1 [3,3][4,1][4] gap=2 (3+3) - 4
        ldmTuple1 [][][][1] --> deleted
        ...
        ldmTuplen [][][][][]
        
        """
        ldmTuple1 = self.part[tupl1Indice] 
        ldmTuple2 = self.part[tupl2Indice] 

        # m times :as many as there are machines
        for m in range(self.m):
            
            # LARGEST : index in the ldmTuple2 so the processor has the largest sum.
            largest = ldmTuple2.largest()
            # SMALEST : ndex in the ldmTuple1 so the processor has the smallest sum.
            smaller = ldmTuple1.smaler()

            #each job from the most loaded processor (of tuple 2), into the least loaded processor (of tuple 1)
            for k in range(ldmTuple2.getProcessor(largest).getJobsSetSize()):
                ldmTuple1.getProcessor(smaller).addJob(ldmTuple2.getProcessor(largest).getJobTime(k))
            # END FOR (for k in range(ldmTuple2.getProcessor(largest).getJobsSetSize()):)

            # raz of tuple 2 processor
            ldmTuple2.getProcessor(largest).razJobsSet()

            # recompute values gap and total
            ldmTuple1.getGap()
            ldmTuple1.getTotal()
            
        # END FOR (for m in range(self.m):)

        # tuple 2 is merged with tuple 1
        # delete tuple 2
        self.part.pop(tupl2Indice)
        

# ########################################################################
#
#                               PSched
#
# Structure to store a scheduling result
# ########################################################################
class PSched:
    # =============================================
    # CONSTRUCTOR
    # =============================================
    def __init__(self, algoName, timeExpected, makespan, time, sched):
        """
        :param algoName     : String name of algoritm
        :param timeExpected : float teorical time expected
        :param makespan     : float Cmax found
        :param time         : float time it took to find Cmax (seconds)
        :param sched        : list (of Processors objects) result of scheduling

        """
        self.algoName     = algoName 
        self.timeExpected = timeExpected 
        self.makespan     = makespan 
        self.time         = time 
        self.sched        = sched
    # =============================================
    # GET  (__str__ not used)
    # =============================================
    def __str__(self):
        return ""

    def getAlgoName(self):
        return self.algoName
    
    def getTimeExpected(self):
        return self.timeExpected
    
    def getMakespan(self):
        return self.makespan

    def getTime(self):
        return self.time
    
    def getSched(self):
        return self.sched

    def getResultHeader():
        return ["algoName", "timeExpected", "makespan", "time"]
    
    def getResult(self):
        """
        return result of schediling
        is call by campaign.py to store it in data frame
        *** can be modified according to the requirements of the results extraction program. ***
        """
        return [self.algoName, self.timeExpected, self.makespan, self.time]
        #return self.algoName, self.timeExpected, self.makespan, self.time

    # =============================================
    # SET  
    # =============================================
    def setAlgoName(self, a):
        self.algoName = a

# #######################################################################
#                                                                       #
#                               FFD2                                     #
# !!! doesn't work !!!                                                    #
# #######################################################################
def ffd2(sizesList, binSize, sortList = False):
    """
    order the given objects in a non-decreasing order
    so that wehaves1≥···≥sn. Initialize a counterN= 0.2.
    Let the bins beB1,···, Bn.
    Put the next (first) object in thefirst “possible” bin ,
    scanning the bins in the orderB1,···, Bn.If a new bin is used, incrementN.
    Return number of bins used, and the binpacking computed
    """
    packing    = []
    binsNumber = 0
    
    #------------------------------------------    
    # work with a copy of costMatrix
    # this matrix will be sorted or modified
    #------------------------------------------
    sizesListW = sizesList[:] 
    if sortList==True:
        # the list is already sorted (if sortList=false)
        sizesListW.sort(reverse = True)
    # END IF    

    # FIRST FIT DECREASING 
    for i in range(len(sizesListW)):
        # Create first bin
        if binsNumber == 0:
            binsNumber+=1
            p = Processor()
            packing.append(p)
        # END IF
        
        # if bin loaded + new size > binSize
        # Must create a new bin
        if packing[binsNumber-1].getTotal() + sizesListW[i] > binSize:
            binsNumber+=1
            p = Processor()
            packing.append(p)
        # END IF
        packing[binsNumber-1].addJob(sizesListW[i])
    # END FOR
    print("FFD==>",binsNumber)
    return binsNumber,packing

# #######################################################################
#                                                                       #
#                               FFD                                     #
#                                                                       #
# #######################################################################
def ffd(sizesList, binSize):
    """
    order the given objects in a non-decreasing order
    so that wehaves1≥···≥sn. Initialize a counterN= 0.2.
    Let the bins beB1,···, Bn.
    Put the next (first) object in thefirst “possible” bin ,
    scanning the bins in the orderB1,···, Bn.If a new bin is used, incrementN.
    Return number of bins used, and the binpacking computed
    """
    #------------------------------------------    
    # work with a copy of costMatrix
    # this matrix will be sorted or modified
    # Sort the list (decreasing)
    #------------------------------------------
    sizesListW = sizesList[:] 
    sizesListW.sort(reverse = True)

    packing    = []
    binsNumber = 0
    
    # FIRST FIT DECREASING 
    for i in range(len(sizesListW)):
        objPacked = False
        for j in range(len(packing)):
            if packing[j].getTotal() + sizesListW[i] <= binSize:
                packing[j].addJob(sizesListW[i])
                objPacked = True
                break
            # END IF
        # END FOR
        if objPacked == False:
            binsNumber+=1
            p = Processor()
            packing.append(p)
            packing[binsNumber-1].addJob(sizesListW[i])
        # END IF
    # END FOR
##    print("Liste en entree")
##    print(sizesListW)
##    print("Packing")
##    print(binSize)
##    for i in range(len(packing)):
##        print("")
##        print(packing[i].getTotal())
##        print(packing[i].jobsSet)
##    input("haha")    
    
    return binsNumber,packing
