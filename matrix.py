import random                    # to use distributions and seed
import statistics        as stat # to compute arithmaetic mean
import scipy.stats       as sc   # to compute harmonic_mean and geometric_mean
import ScheduleManagment as sm   # to retrieve PSchedHeader
import setup             as s    # 

# tools libraries
import pwa
# ############################################################################
# ############################################################################
#                               PTimes class
# ############################################################################
# ############################################################################
class PTimes:
    """
    management of the PTimes object: time list. 
    """
    # ############################################################################
    #
    #                               CONSTRUCTOR
    #
    # ############################################################################
    def __init__(self, generateMethode, n, m, a=1.0, b=100.0, alpha=1.0, beta=1.0, lambd=1.0, fileName="", seed = None):
        """
        :param generateMethode: STRING describe how this list is generated.
                                "GAMMA"
                                "BETA"
                                "EXPONENTIAL"  
                                "UNIFORM"      uniform instencies generation LORI and MARTELLO)
                                "NON_UNIFORM"  non uniform instencies generation LORI and MARTELLO)
                                "REAL"         from workload archive - www.cs.huji.ac.il/labs/parallel/workload
        :param m              : Int Machine number. 0 <= m < n. 0 if problemType = "P" and completedM1 = False
        :param a              : int = 1     a value for uniform and non uniform generation
        :param b              : int = 100   b value for uniform and non uniform generation
        :param alpha          : float = 1.0 alpha value for beta and gamma generation
        :param beta           : float = 1.0 beta value for gamma generation (beta value for beta is equal 1)
        :param lamlbd         : float = 1.0 lambda value for exponential generation
        :param fileName       : String  = [](complete filename) for PWA (Parallel Workload Archive) import
        :param seed           : Int   = None
                                    if none : seed is randomly (random library) générated, and used to générate times list
                                    if set  : seed is used to retrieve and regenerate a previously generated time list.
        ----------------------------------------------------
        List and Computed results with original times List
        ----------------------------------------------------
        :param Times                         : List   : of Pj : set of times   : [e1, e2, ... en]
        :param n                             : Integer: Jobs number. n > 0 for the original
        ----------
        :param LowBound                      : Float  : known low bound
        :param StatIndicators                : tuple of Floats  : meanPerMachine, Work_Time, mean (Arithmetical),mean (Geometric);mean (harmonic);median;mode,minimum,maximum,standard_deviation,variance
        ----------
        :param Results                       : tuples list of the results obtained with each algorithm, from the original time list.
                                           [(ALGORITHM1, computed makespan, computation time, resultMatrix []),...,(ALGORITHMp, computed makespan, computation time, resultMatrix[])]
        :param BestResult_Makespan           : Float  : Best Makespan obtained (closer to the lower bound)
        :param BestResult_MakespanAlgorithm  : String : Which algo got the best Makespan
        :param BestResult_Time               : float  : Best Time obtained (lower time)
        :param BestResult_TimeAlgorithm      : String : Which algo got the best time

        ----------------------------------------------------
        List and Computed results with times List completed with m-1 job times
        ----------------------------------------------------
        :param Times                         : List   : of Pj : set of times   : [e1, e2, ... en']
        :param m1_n                          : Integer: new number of times set
        ----------    
        :param m1LowBound                    : Float  : known low bound
        :param m1StatIndicators                : tuple of Floats  : meanPerMachine, Work_Time, mean (Arithmetical),mean (Geometric);mean (harmonic);median;mode,minimum,maximum,standard_deviation,variance
        :param m1Optimal                     : Float  : known optimal 
        ----------
        :param m1Results                     : Tuples List of the results obtained with each algorithm, from the completed time list.
                                               [(ALGORITHM1, computed makespan, computation time, resultMatrix []),...,(ALGORITHMp, computed makespan, computation time, resultMatrix[])]
        :param m1BestResult_Makespan         : FLOAT  : Best Makespan obtained (closer to the known m1Optimal)
        :param m1BestResult_MakespanAlgorithm: String : Which algo got the best Makespan
        :param m1BestResult_Time             : Float  : Best Time obtained (lower time)
        :param m1BestResult_TimeAlgorithm    : String :Which algo got the best time
        create Lists instances with

        ************************************ __INIT__ method ************************************

        # Input -----------------------------------
        :param generateMethode: STRING describe how this matrix is generated. 
        :param n              : Integer Jobs number. n > 0
        :param m              : Integer Machine number. 0 <= m < n. 0 if problemType = "P" and completedM1 = False
        :param a              : Float   a value for uniform and non uniform generation
        :param b              : Float   b value for uniform and non uniform generation
        :param alpha          : Float   alpha value for beta and gamma generation
        :param beta           : Float   beta value for gamma generation (beta value for beta is equal 1)
        :param lamlbd         : Float   lambda value for exponential generation
        :param fileName       : String  (complete filename) for PWA (Parallel Workload Archive) import
        :param seed           : Integer if none : seed is randomly (random library) générated, and used to générate times list
                                        if set  : seed is used to retrieve and regenerate a previously generated time list.

        # Computed --------------------------------
        Times                 
        n                     
        LowBound
        m1Times                 
        m1_n
        m1LowBound
        m1Optimal
        
        # Output ---------------------------------
        nichts
        """
        # =======================================================================
        # generation properties
        # =======================================================================
        self.generateMethode                = generateMethode
        self.m                              = m
        #-------------------------------------------------------
        # 
        #-------------------------------------------------------
        self.a                              = a
        self.b                              = b
        self.alpha                          = alpha
        self.beta                           = beta
        self.lambd                          = lambd      # not lambda (with a) because reserved word 
        self.fileName                       = fileName
        #-------------------------------------------------------
        # SEED
        #-------------------------------------------------------
        if seed:
            self.seed = seed
        else:
            self.seed = random.randint(1,10000)
        # END IF

        # =======================================================================
        # Times set
        # =======================================================================

        # #1# origin problem instance (not completed)
        self.Times                          = []
        self.n                              = n
        self.LowBound                       = 0.0
        self.StatIndicators                 = []
        self.Results                        = []
        self.BestResult_Makespan            = 0.0
        self.BestResult_MakespanAlgorithm   = ""
        self.BestResult_Time                = 0.0
        self.BestResult_TimeAlgorithm       = ""

        # completed problem instance (with m-1 tasks completion)
        self.m1Times                        = []
        self.m1_n                           = 0
        self.m1LowBound                     = 0.0
        self.m1StatIndicators               = []
        self.m1Optimal                      = 0.0
        self.m1Results                      = []
        self.m1BestResult_Makespan          = 0.0
        self.m1BestResult_MakespanAlgorithm = ""
        self.m1BestResult_Time              = 0.0
        self.m1BestResult_TimeAlgorithm     = ""

        #-------------------------------------------------------
        # use of pseudo-random number generator
        #-------------------------------------------------------
        if (self.generateMethode == "UNIFORM"):
            # UNIFORM P: 
            self.Times = uniform_p(n,self.seed, a,b)
        elif (self.generateMethode == "NON_UNIFORM"):
            # NON_UNIFORM P:
            self.Times  = non_uniform_p(n,self.seed,a, b)
        elif (self.generateMethode == "GAMMA"):
            # GAMMA P: problem not considered at this time.
            self.Times  = gamma_p(n,self.seed,alpha, beta)
        elif (self.generateMethode == "BETA"):
            # BETA P:
            self.Times  = beta_p(n,self.seed,alpha)
        elif (self.generateMethode == "EXPONENTIAL"):
            # EXPONENTIAL P: 
            self.Times  = exponential_p(n,self.seed,lambd)
        # END IF    

        #-------------------------------------------------------
        # Use of a reel case
        #-------------------------------------------------------

        # REAL : Real, According the "parallel work load archive"
        #elif (self.generateMethode == "REEL"):
        else:
            self.Times  = real_p(fileName)
            
        # ENDIF

        #-------------------------------------------------------
        # 
        #-------------------------------------------------------
        self.LowBound = getLowBound(self.Times, self.m)
        self.StatIndicators = getStatIndicators(self.Times, self.m)
        
        # =======================================================================
        # self.m1Times generation
        # =======================================================================
        self.completeM1(m)

    # ############################################################################
    #
    #                               METHODS
    #
    # ############################################################################

    # ============================================================================
    # completeM1 
    # ============================================================================
    def completeM1(self, m):
        """
        set self.m number of machines 
        Complete list Times with m-1 job times in list m1Times
        # input
        m number of machines
        # Compute
        m1Times
        m1Optimal,
        m1_n,
        """
        #------------------------------------------------------------------------
        # SET
        #------------------------------------------------------------------------
        self.m = m 

        #------------------------------------------------------------------------
        #   INIT
        #------------------------------------------------------------------------
        proc   = []               # work with processors list len(proc) <= m
        
        #------------------------------------------------------------------------
        #   matrixOrigin --> matrix
        #------------------------------------------------------------------------
        self.m1Times = self.Times[:]  # self.m1Times = tools.matrix1dCopy(self.Times)
        new_n = self.n
        
        #------------------------------------------------------------------------
        # Scrolls through the "self.matrix" list to
        # fill in the processor load list "proc"
        #------------------------------------------------------------------------
        for i in range(len(self.Times)):
            if (len(proc) < self.m):
                proc.append(float(self.Times[i]))
            else:
                # sorts the proc list and fills in the first one which is the smallest.
                proc.sort()  
                proc[0] = float(proc[0]) + float(self.Times[i])
            # END IF
        # END FOR

        #------------------------------------------------------------------------
        # sorts the list proc in the rerverse order.
        # The first element is the most loaded :
        # fill in the remain self.m&Times to obtain same Cmax on all proc[x]
        #------------------------------------------------------------------------
        proc.sort(reverse=True)
        Cmax = proc[0]
        for i in range(len(proc)):
            if (i > 0):
                self.m1Times.append(Cmax - proc[i])
                new_n += 1
            # END IF
        # END FOR

        #------------------------------------------------------------------------
        #   Update self concerned values
        #------------------------------------------------------------------------
        self.m1_n               = new_n
        self.m1LowBound         = getLowBound(self.m1Times, self.m)
        self.m1StatIndicators   = getStatIndicators(self.Times, self.m)
        self.m1Optimal          = Cmax

    # ============================================================================
    # GET SEED
    # ============================================================================
    def getSeed(self):
        return self.seed
    
    # ============================================================================
    # ADD RESULTS addSched
    # ============================================================================
    def addSched(self, sched):
        self.Results.append(sched)
        
        # for best time algorithm
        if (sched.getTime() < self.BestResult_Time) or (self.BestResult_Time == 0.0):
            self.BestResult_Time              = sched.getTime()
            self.BestResult_TimeAlgorithm     = sched.getAlgoName()
        # END IF

        # for best sched Cmax algorithm
        if (sched.getMakespan() < self.BestResult_Makespan) or (self.BestResult_Makespan == 0.0):
            self.BestResult_Makespan          = sched.getMakespan()
            self.BestResult_MakespanAlgorithm = sched.getAlgoName()
        # END IF

    # ============================================================================
    # ADD RESULTS addM1Sched
    # ============================================================================
    def addM1Sched(self, sched):
        self.m1Results.append(sched)

        # for best time algorithm
        if (sched.getTime() < self.m1BestResult_Time)  or (self.m1BestResult_Time == 0.0):
            self.m1BestResult_Time              = sched.getTime()
            self.m1BestResult_TimeAlgorithm     = sched.getAlgoName()
        # END IF

        # for best sched Cmax algorithm
        if (sched.getMakespan() < self.m1BestResult_Makespan) or (self.m1BestResult_Makespan == 0.0):
            self.m1BestResult_Makespan          = sched.getMakespan()
            self.m1BestResult_MakespanAlgorithm = sched.getAlgoName()
        # END IF
    # ============================================================================
    #  getResult
    #  Summary for pandas dataframe
    # ============================================================================
    def getResult(self):
        res = [self.generateMethode, self.m, self.seed, self.n, self.LowBound, self.m1_n, self.m1LowBound, self.m1Optimal]
        #----------------------------------------
        # Results and m1Results lists structures
        #
        # [(ALGORITHM1, computed makespan, computation time, resultMatrix []),...,(ALGORITHMp, computed makespan, computation time, resultMatrix[])]
        #----------------------------------------
        res.append("Results")
        for k in range(len(self.Results)):
            sc = self.Results[k].getResult()    # self.Results[k] = sched object
            res.append(sc)  
        # END FOR

        res.append("m1Results")
        for k in range(len(self.m1Results)):
            sc = self.m1Results[k].getResult()  # self.m1Results[k].getResult() = sched object
            res.append(sc) 
        # END FOR
        
        #res = (self.generateMethode, self.n, self.m,self.a, self.b, self.alpha, self.beta, self.lambd, self.fileName, self.seed)
        return res
    
    # ============================================================================
    #  getResultForCSVHeader
    # ============================================================================
    def getResultForCSVHeader():
        lstHeader       = ["generateMethode", "m", "seed", "n", "LowBound", "m1_n", "m1LowBound", "m1Optimal"]
        lstSep          = ["resultConcerns"]
        lstPSchedHeder  = sm.PSched.getResultHeader()
        return lstHeader + lstSep +lstPSchedHeder

    # ============================================================================
    #  getResultForCSV
    #  constructs one list item per algorithm result, and per list type (native or completed)
    # ============================================================================
    def getResultForCSV(self):
        listReturn = []
        oriRes = [self.generateMethode, self.m, self.seed, self.n, self.LowBound, self.m1_n, self.m1LowBound, self.m1Optimal]
        
        #----------------------------------------
        # Results and m1Results lists structures
        # [
        # [...... RESULTS,   ALGORITHM1, computed makespan, computation time, resultMatrix[]
        # [...... M1RESULTS, ALGORITHMp, computed makespan, computation time, resultMatrix[]
        # ]
        #----------------------------------------
        for k in range(len(self.Results)):
            res = oriRes[:]
            res.append("Results")
            
            sc = self.Results[k].getResult()    # self.Results[k] = sched object
            for i in range(len(sc)):
                res.append(sc[i])
            # END FOR
            listReturn.append(res)
        # END FOR

        for k in range(len(self.m1Results)):
            res = oriRes[:]
            res.append("m1Results")
            sc = self.m1Results[k].getResult()  # self.m1Results[k].getResult() = sched object
            for i in range(len(sc)):
                res.append(sc[i])
            # END FOR
            listReturn.append(res)
        # END FOR
        
        #res = (self.generateMethode, self.n, self.m,self.a, self.b, self.alpha, self.beta, self.lambd, self.fileName, self.seed)
        return listReturn
        
    # ============================================================================
    #  getResultDetailed 
    #  for pandas dataframe
    # ============================================================================
    def getResultDetailed(self):
        res = [self.generateMethode,
               self.m, self.a, self.b, self.alpha, self.beta, self.lambd, self.fileName, self.seed,
               self.n,    self.LowBound,    self.StatIndicators,   self.BestResult_MakespanAlgorithm,   self.BestResult_Makespan,    self.BestResult_TimeAlgorithm,   self.BestResult_Time,   
               self.m1_n, self.m1LowBound,  self.m1StatIndicators, self.m1BestResult_MakespanAlgorithm, self.m1BestResult_Makespan,  self.m1BestResult_TimeAlgorithm, self.m1BestResult_Time, self.m1Optimal]
        #----------------------------------------
        # Results and m1Results lists structures
        #
        # [(ALGORITHM1, computed makespan, computation time, resultMatrix []),...,(ALGORITHMp, computed makespan, computation time, resultMatrix[])]
        #----------------------------------------
        res.append("Results")
        for k in range(len(self.Results)):
            sc = self.Results[k].getResult()    # self.Results[k] = sched object
            res.append(sc)  
        # END FOR

        res.append("m1Results")
        for k in range(len(self.m1Results)):
            sc = self.m1Results[k].getResult()  # self.m1Results[k].getResult() = sched object
            res.append(sc) 
        # END FOR
        
        #res = (self.generateMethode, self.n, self.m,self.a, self.b, self.alpha, self.beta, self.lambd, self.fileName, self.seed)
        return res

# ############################################################################
# ############################################################################
#
#                    Time lists generation with seeds management
#
# ############################################################################
# ############################################################################
def uniform_p(n,seed, a,b):
    matrix = []

    random.seed(seed)
    for i in range(n):
        rand = random.uniform(a,b)
        if s.INT_UNIFORM: rand = round(rand)    # float or integer
        matrix.append(rand)
    # END FOR    
    return matrix

def non_uniform_p(n,seed, a,b):
    matrix = []
    random.seed(seed)
    #
    n98 = int((98*n) / 100)
    a1 = 0.9*(b-a)
    b1 = b
    a2 = a
    b2 = 0.2*(b-a)
    for i in range(n98):
        rand = random.uniform(a1,b1)
        if s.INT_NON_UNIFORM: rand = round(rand)    # float or integer
        matrix.append(rand)
    # END FOR
    for i in range(n-n98):
        rand = random.uniform(a2,b2)
        if s.INT_NON_UNIFORM: rand = round(rand)    # float or integer
        matrix.append(rand)
    # END FOR    
    return matrix

def gamma_p(n,seed, alpha,beta):
    matrix = []
    random.seed(seed)
    for i in range(n):
        rand = random.gammavariate(alpha,beta)
        matrix.append(rand)
    # END FOR        
    return matrix

def beta_p(n,seed, alpha):
    """
    beta allways 1 for this set
    """
    matrix = []
    random.seed(seed)
    for i in range(n):
        rand = random.betavariate(alpha,1)
        matrix.append(rand)
    # END FOR        
    return matrix

def exponential_p(n,seed, lambd):
    matrix = []
    random.seed(seed)
    for i in range(n):
        rand = random.expovariate(lambd)
        matrix.append(rand)
    # END FOR        
    return matrix

def real_p(fileName):
    matrix = pwa.pwaFileRead(fileName)
    return matrix

# ############################################################################
# ############################################################################
#
#                    Statistics for times lists
#
# ############################################################################
# ############################################################################

# ============================================================================
# LowBound : max(largest time, mean time per machine/processor)
# ============================================================================
def getLowBound(l, m):
    if m != 0:
        return max(max(l), sum(l)/m)
    else:
        return max(max(l))

# ============================================================================
# getWorkTime : Total work  
# ============================================================================
def getWorkTime(l):
    return sum(l)

# ============================================================================
#  getMeanTime : Mean Work
# ============================================================================
def getMeanTimePerMachine(l, m):
    if m != 0:
        return sum(l)/m
    else:
        return 0
# ============================================================================
# getIndicators
# descriptive statistical indicators.
#
# return tuple
#   Related to the problem*
#       meanPerMachine,
#       Work_Time, 
#   Descriptive
#       mean (Arithmetical)
#       mean (Geometric)
#       mean (harmonic)
#       median
#       Mode
#       Minimum
#       Maximum
#   Dispersion
#       Standard Deviation  (with mu = arithmetic mean)  fr:écart type
#       Variance            (with mu = arithmetic mean) 
#       not the Quartiles
# ============================================================================
def getStatIndicators(l, m):
    """
    input
      l : List : set of times
      m : int. Number of parallel machines
    Return a tuple with followings values
      meanPerMachine, Work_Time, mean (Arithmetical), mean (Geometric); mean (harmonic); median; mode, minimum, maximum, standard_deviation, variance
    """
    # ----------------------------------------------------------
    # mu
    # to call it one time (used in mean, pstdev and pvariance)
    # if this parameter is not injected into pstdev and pvariance,
    # these functions re compute the mean.
    # ----------------------------------------------------------
    mu = stat.mean(l)
    return (    getMeanTimePerMachine(l, m),
                getMeanTimePerMachine(l, m),
                stat.mean(l),
                sc.gmean(l),
                sc.hmean(l),
                stat.median(l),
                min(l), max(l),
                stat.pstdev(l,mu),
                stat.pvariance(l, mu))

    # stat.mode(l),
