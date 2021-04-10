import time
import math
from operator import attrgetter
#
import matrix as cm
import ScheduleManagment as sm # Processor object / PSched object / algorithms tools


# #######################################################################
#                                                                       #
#                               LPT                                     #
#                                                                       #
# #######################################################################
def lpt(costMatrix, m):
    """
    Compute a schedule with LPT rule algorithm.
    Input
      costMatrix : matrix (1 dimension) conaining a set of n jobs cost time
      m          : number of machines
    Output
      tuple of 5 items:
        algoName     : name of algorithm
        timeExpected : the time expected computed with algorithm complexity
        makespan     : makesapn comuted
        time         : the time it took to calculate the makespan
        sched        : in the form of a Processor object list. Each "Processor" object represents the load of a machine, with the total time and a list of each job cost allocated to that processor.
    """
    
    print("Begin LPT Number of machines :",m)
    algoName = "LPT"

    #------------------------------------------    
    # work with a copy of costMatrix
    # this matrix will be sorted or modified
    #------------------------------------------    
    matrixW = costMatrix[:] # tools.matrix1dCopy(costMatrix)

    #------------------------------------------    
    # Time expected, according time complexity 
    #------------------------------------------
    n = len(matrixW)
    timeExpected = n * math.log(n) + n * math.log(m)

    #------------------------------------------    
    # sched is a list of Processor objects.
    #------------------------------------------    
    sched= [] 

    #------------------------------------------    
    # current time at the bégining
    #------------------------------------------    
    before = time.time()

    #==========================================    
    # LPT RULE 
    #==========================================    

    #------------------------------------------    
    # sort matrix by non - increasing costs
    #------------------------------------------    
    matrixW.sort(reverse=True)

    #==========================================    
    # Sched calculation
    #==========================================    
    for i in range(n):
        #------------------------------------------    
        # The maximum number of processors (or machines) is not reached.
        # One more processor is added for each iteration.
        #------------------------------------------    
        if (len(sched) < m):
            p = sm.Processor()
            p.addJob(matrixW[i])
            sched.append(p)
            
        else:
            #------------------------------------------    
            # The maximum number of processors (or machines) is reached.
            # Each cost is allocated to the least loaded
            # processor (machine) at this time.
            #------------------------------------------    
            sched.sort(key=attrgetter("jobsTotal"))
            sched[0].addJob(matrixW[i])
            

    #------------------------------------------            
    # current time at the bégining
    #------------------------------------------    
    after = time.time()

    #------------------------------------------            
    # Retrieve Makespan (most loaded machine)
    #------------------------------------------    
    makespan = 0.0
    for i in range(len(sched)):
        makespan = max(makespan, sched[i].jobsTotal)

    #------------------------------------------
    # RETURN Makespan obtained /
    #        Processing algorithm time /
    #        Schedul 
    #------------------------------------------
    timeAlgo = after-before
    res = sm.PSched(algoName, timeExpected, makespan, timeAlgo, sched)
    return res
    

# #######################################################################
#                                                                       #
#                               SLACK                                   #
#                                                                       #
# #######################################################################
def slack(costMatrix, m):
    """
    Compute a schedule with SLACK algorithm.
    Input
      costMatrix : matrix (1 dimension) conaining a set of n jobs cost time
      m          : number of machines
    Output
      tuple of 5 items:
        algoName     : name of algorithm
        timeExpected : the time expected computed with algorithm complexity
        makespan     : makesapn comuted
        time         : the time it took to calculate the makespan
        sched        : in the form of a Processor object list. Each "Processor" object represents the load of a machine, with the total time and a list of each job cost allocated to that processor.
    """
    print("Begin SLACK Number of machines :",m)
    
    #------------------------------------------
    #
    #------------------------------------------
    algoName = "SLACK"
    timeExpected = 0.0
    
    #------------------------------------------    
    # work with a copy of costMatrix
    # this matrix will be sorted or modified
    #------------------------------------------
    matrixW = costMatrix[:] # tools.matrix1dCopy(costMatrix)
    
    #------------------------------------------    
    # sched is a list of Processor objects.
    #------------------------------------------
    makespan = 0.0
    sched= []

    #------------------------------------------    
    # current time at the bégining
    #------------------------------------------    
    before = time.time()

    #==========================================    
    # GREEDY Approach
    #==========================================    

    #------------------------------------------    
    # SORT Jobs cost by non increasing costs
    #------------------------------------------    
    matrixW.sort(reverse=True)
    
    #------------------------------------------    
    # Cutting of the starting matrix in n/m under dies of size m each.
    # result is a list of Processors objects of m item each.
    # NB
    # We use the object Processor structure because the matrixWSlack will be sorted by non increasing jobsGap value
    #------------------------------------------
    # subsetSize = math.ceil(len(matrixW)/m) to keep command
    #------------------------------------------
    matrixGreedy = [] 

    itemNb = 0
    subsetNumbers = 0
    
    for i in range(len(matrixW)):
        #
        itemNb+=1
        # 
        if (itemNb > m):
            itemNb = 1
            subsetNumbers+=1
            
        # end if    
        if (itemNb == 1):
            p = sm.Processor()
            p.addJob(matrixW[i])
            matrixGreedy.append(p)
        else:
            matrixGreedy[subsetNumbers].addJob(matrixW[i])
        # end if
    #------------------------------------------    
    # SORT subsets by non increasing jobsGap value
    #------------------------------------------
    matrixGreedy.sort(key=attrgetter("jobsGap"), reverse=True)

    #------------------------------------------    
    # flattening the job list. (in matrixWSlack)
    #------------------------------------------
    matrixWSlack = []
    for i in range(len(matrixGreedy)):
        for j in range(len(matrixGreedy[i].jobsSet)):
            matrixWSlack.append(matrixGreedy[i].jobsSet[j])
        # end for
    # end for
    
    #==========================================    
    # COMPUTE PART (like LPT)
    # work with matrixWSlack
    #==========================================    
    for i in range(len(matrixWSlack)):
        #------------------------------------------    
        # The maximum number of processors (or machines) is not reached.
        # One more processor is added for each iteration.
        #------------------------------------------    
        if (len(sched) < m):
            p = sm.Processor()
            p.addJob(matrixWSlack[i])
            sched.append(p)
            
        else:
            #------------------------------------------    
            # The maximum number of processors (or machines) is reached.
            # Each cost is allocated to the least loaded
            # processor (machine) at this time.
            #------------------------------------------    
            sched.sort(key=attrgetter("jobsTotal"))
            sched[0].addJob(matrixWSlack[i])
        # END IF
    # END FOR
    
    #------------------------------------------    
    # current time at the end
    #------------------------------------------    
    after  = time.time()

    #------------------------------------------            
    # Retrieve Makespan (most loaded machine)
    #------------------------------------------    
    makespan = 0.0
    for i in range(len(sched)):
        makespan = max(makespan, sched[i].jobsTotal)

    #------------------------------------------
    # RETURN Makespan obtained /
    #        Processing algorithm time /
    #        Schedul 
    #------------------------------------------
    timeAlgo = after-before
    res = sm.PSched(algoName, timeExpected, makespan, timeAlgo, sched)
    return res

# #######################################################################
#                                                                       #
#                               LDM                                     #
#                                                                       #
# !!!!!!!! Dont work : issue of lists addresses                         #
# #######################################################################
def ldm(costMatrix, m):
    """
    Compute a schedule with LDM algorithm.
    Input
      costMatrix : matrix (1 dimension) conaining a set of n jobs cost time
      m          : number of machines
    Output
      tuple of 5 items:
        algoName     : name of algorithm
        timeExpected : the time expected computed with algorithm complexity
        makespan     : makesapn comuted
        time         : the time it took to calculate the makespan
        sched        : in the form of a Processor object list. Each "Processor" object represents the load of a machine, with the total time and a list of each job cost allocated to that processor.
    """
    print("Begin LDM Number of machines :",m)
    
    #------------------------------------------
    #
    #------------------------------------------
    algoName = "LDM"
    timeExpected = 0.0
    
    #------------------------------------------    
    # work with a copy of costMatrix
    # this matrix will be sorted or modified
    #------------------------------------------
    matrixW = costMatrix[:] # matrixW = tools.matrix1dCopy(costMatrix)
    
    #------------------------------------------    
    # sched is a list of Processor objects.
    #------------------------------------------
    makespan = 0.0
    sched= []

    #------------------------------------------    
    # current time at the bégining
    #------------------------------------------    
    before = time.time()

    #==========================================    
    # NUMBERS PARTITIONNING Approach
    #==========================================
    
    #------------------------------------------    
    # list (partition.part) of m-tuples creation
    #------------------------------------------
    partition = sm.ldmPartition(matrixW, m)

    while partition.getPartSize() > 1:
        #------------------------------------------    
        # SORT list partition.part  by non increasing tuplGap value
        #------------------------------------------
        partition.partSortBytuplGapDec()

        #------------------------------------------
        # the first two partition.part[0] and partition.part[1]
        # are the m-tuples with the largest difference.
        # we merge these two
        #------------------------------------------
        partition.partMerge(0,1)
    # END WHILE

    #------------------------------------------    
    # current time at the end
    #------------------------------------------    
    after  = time.time()

    #------------------------------------------            
    # Retrieve Makespan (most loaded machine)
    #------------------------------------------    
    makespan = 0.0
    sched = partition.getSched()
    for i in range(len(sched)):
        makespan = max(makespan, sched[i].jobsTotal)
    #------------------------------------------
    # RETURN Makespan obtained /
    #        Processing algorithm time /
    #        Schedul 
    #------------------------------------------
    timeAlgo = after-before
    res = sm.PSched(algoName, timeExpected, makespan, timeAlgo, sched)
    return res

# #######################################################################
#                                                                       #
#                               COMBINE                                 #
# need FFD algorithm                                                    #
# #######################################################################
def combine(costMatrix, m, alpha = 0.005):
    """
    alpha = 0.005 
    """
    print("Begin COMBINE Number of machines :",m)
    algoName = "COMBINE"

    #------------------------------------------    
    # work with a copy of costMatrix
    # this matrix will be sorted or modified
    #------------------------------------------
    matrixW = costMatrix[:] # matrixW = tools.matrix1dCopy(costMatrix)
    
    #------------------------------------------    
    # sched is a list of Processor objects.
    #------------------------------------------
    makespan = 0.0
    sched= []

    #------------------------------------------    
    # current time at the bégining
    #------------------------------------------    
    before = time.time()
    matrixW.sort(reverse=True)
    
    #------------------------------------------    
    # Bounds for binary search
    #------------------------------------------
    i          = 0
    iMax       = 200
    #
    n          = len(matrixW)
    A          = sum(matrixW)/m
    PSchedLPT  = lpt(matrixW, m)    # is a PSched
    M          = PSchedLPT.getMakespan()
    Mm         = (M / ( (4/3) - (1 / (3*m) ) ))
    p1         = matrixW[0]
    mFFD = 0
    
    if M >= 1.5 * A:
        #==========================================
        # LPT part.
        #==========================================

        # i = 1                         # useless : LPT return result (TimeExpected to) i <> 0 if a log(i) used. 
        PSchedLPT.setAlgoName(algoName) # should be corrected, as it was LPT that gave the answer
        return PSchedLPT
    
    else:
        #==========================================
        # MULTIFIT part.
        # with bounds as follow Ub = Cmax(LPT)
        #                       Lb = max(A, p1, Mm)
        # Stopping condition    when Ub - Lb <= alpha . A
        #==========================================

        #------------------------------------------
        # BOUNDS
        #------------------------------------------
        cu = M               # LPT result
        cl = max(A, p1, Mm)  #

        # dirty fiddling ! just for test 
        mFFDU, sched = sm.ffd(matrixW, cu)
        if mFFDU > m: cu = 1.1*M
        # dirty fiddling ! just for test 
         
        #------------------------------------------
        # MULTIFIT part. 
        # while cu - cl > alpha * A:
        # to force at least once
        #------------------------------------------
        while True:

            mFFDL, sched = sm.ffd(matrixW, cl)
            print("=====> ", mFFDU, cu, mFFDL)

                            
            i+=1
            c = (cu + cl)/2
            mFFD, sched = sm.ffd(matrixW, c)
            if mFFD <= m:
                cu = c
            else:
                cl = c
            # END IF
            
            #------------------------------------------
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            # * mFFD == m is an additional condition
            # to force the algorithm to give a good answer.
            # * i > iMax is an additional condition
            # to avoid infinite loops
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            #------------------------------------------
            if ((cu - cl <= alpha * A) and (mFFD == m)) or (i>iMax):
            #if ((cu - cl <= alpha * A)) or (i>iMax):
                if i > iMax:
                    algoName = "COMBINE STOPED (binary search)"
                    print("!!! COMBINE STOPED (BINARY SEARCH) because number of iterations too large !!!", i)
                # END IF
                break
            # END IF
            
        # END WHILE
    # END IF
    
    #------------------------------------------    
    # current time at the end
    #------------------------------------------    
    after = time.time()

    #------------------------------------------            
    # Retrieve Makespan
    # makespan is not most loaded machine, but cu
    # see above
    #------------------------------------------    
    #for i in range(len(sched)):
    #    makespan = max(makespan, sched[i].jobsTotal)
    #------------------------------------------            
    # makespan = cu (by combine definition)
    #------------------------------------------    
    makespan = cu


    #------------------------------------------    
    # the expected time is also relative to i
    #------------------------------------------    
    timeExpected = (n * math.log(n)) + (i * n * math.log(m))

    #------------------------------------------
    # RETURN Makespan obtained /
    #        Processing algorithm time /
    #        Schedul 
    #------------------------------------------
    timeAlgo = after-before
    res = sm.PSched(algoName, timeExpected, makespan, timeAlgo, sched)
    return res

# #######################################################################
#                                                                       #
#                               MULTIFIT                                #
#                                                                       #
#                                                                       #
# used by COMBINE                                                       #
# #######################################################################
def multifit(sizeList, m, k=8):
    """
    :param sizeList :
    :param m        : 
    :param cLow     :
    :param cUpper   :
    :param k        :
    """
    print("Begin MULTIFIT Number of machines :",m)
    algoName = "MULTIFIT"
    timeExpected = 0.0

    #------------------------------------------    
    # work with a copy of costMatrix
    # this matrix will be sorted or modified
    # sizesList is sorted 
    #------------------------------------------
    sizesListW = sizeList[:]


    #------------------------------------------    
    # current time at the bégining
    #------------------------------------------    
    before = time.time()

    sizesListW.sort(reverse=True)

    # iteration binary search (max k, or max iMax)
    i = 0
    
    n = len(sizesListW)
    A  = sum(sizesListW)/m
    cl = max(sizesListW[0], A)
    cu = max(sizesListW[0], 2*A)

    #------------------------------------------    
    # Binary search
    #------------------------------------------
    iMax = 200
    while True: #while i <= k:
        i+=1
        c = (cu + cl)/2
        mFFD, packing = sm.ffd(sizesListW, c)
        if mFFD <= m:
            cu = c
        else:
            cl = c
        # END IF

        #------------------------------------------
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # * mFFD == m is an additional condition
        # to force the algorithm to give a good answer.
        # * i > iMax is an additional condition
        # to avoid infinite loops
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #------------------------------------------
        if (i >= k and mFFD == m) or (i > iMax):
            if i > iMax:
                algoName = "MULTIFIT STOPED (binary search)"
                print("!!! MULTIFIT STOPED (BINARY SEARCH) because number of iterations too large !!!", i)
            break
    # END WHILE

    #------------------------------------------    
    # current time at the end
    #------------------------------------------    
    after = time.time()

    #------------------------------------------            
    # Retrieve Makespan
    # makespan = cu (by multifit definition)
    #------------------------------------------    
    makespan = cu
    sched = packing[:]

    #------------------------------------------            
    # Retrieve Makespan
    # makespan is not most loaded machine, but cu
    # see above
    #------------------------------------------    
    #for i in range(len(sched)):
    #    makespan = max(makespan, sched[i].jobsTotal)

    #------------------------------------------    
    # the expected time is also relative to i
    #------------------------------------------    
    timeExpected = (n * math.log(n)) + (i * n * math.log(m))

    #------------------------------------------
    # RETURN Makespan obtained /
    #        Processing algorithm time /
    #        Schedul 
    #------------------------------------------
    timeAlgo = after-before
    res = sm.PSched(algoName, timeExpected, makespan, timeAlgo, sched)
    return res
