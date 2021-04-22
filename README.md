# Evaluation of scheduling algorithms

## Table of Contents
1. [General Info](#general-info)
2. [Prerequisites](#prerequisites)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Collaboration](#collaboration)

### General Info
***
![Image text](http://ctu.univ-fcomte.fr/sites/ctu/files/inline-images/SUP_final2020_nom.png)

#### Evaluation of scheduling algorithms.

The goal of this project is to evaluate and compare scheduling algorithms for the P||Cmax problem.  
First, job cost instances are either randomly generated according to distribution functions such as the uniform function, the gamma function, and the beta function, or retrieved from real job logs, from a Parallel Worklaod Archive. Then these instances are subjected to the LPT, SLACK, LDM and COMBINE algorithms.

#### project status

Documents || implementation
:----- | ----- | :-----
itsefl | : | done
user's manual | : | **not started**
report | : | **in progress**
||
||

Algorithm || implementation
:----- | ----- | :-----
LPT | : | functional
SLACK | : | functional
LDM | : | functional
COMBINE | : | functional
||
||

instances generation || implementation | with seed management
:----- | ----- | :----- | :-----
uniform | : | functional | yes
non-uniform | : | functional | yes
lambda | : | functional | yes
beta | : | functional | yes
exponential | : | functional | yes
Parallel Workload Archive | : | functional | no
|||
|||

Module || implementation
:----- | ----- | :-----
result csv file export  | : | functional
results statistics gui | : | **in progress**

## Prerequisites
***
The project uses a number of libraries, plug-ins, editors and other technologies that must be installed beforehand. 
The programs are tested and work with the announced versions (e.g. Python 3.4)  
The installation procedure is given for a Linux environment using the APT package manager (more specifically Debian 8.11). you will have to adapt the installation commands to the target environment. 

List of technologies used within the project:

* first and foremost :
```
$ sudo apt-get update
```

* [Python](https://www.python.org/): Version 3.4 
```
$ sudo apt-get install python3.4
$ sudo apt-get install python3.4-minimal
$ sudo apt-get install idle-python3.4 
```

* [pandas library](https://pandas.pydata.org/): Version 0.14.1-2
```
$ sudo apt-get install python3-pandas 
$ sudo apt-get install python3-pandas-lib
```

* [R Langage](https://cran.rstudio.com/): 3.5.3.1
```
$ sudo apt-get install r-base 
$ sudo apt-get install r-base-dev
```

* [rStudio](https://rstudio.com/solutions/r-and-python/): Version 1.1.463
	+ follow this [link](https://www.rstudio.com/products/rstudio/download/#download) 
		- download the appropriate version  
		- OR, for Debian 8.11 environment,  follow the [older versions](https://www.rstudio.com/products/rstudio/older-versions/) link :   
			and download the [rstudio-1.1.463-amd64.deb](https://download1.rstudio.org/rstudio-1.1.463-amd64.deb) file  
	+ right click on the .deb file
	+ installation program *apper* [^1] 

* ggplot2 / readr / dplyr (RStudio version must be 3.5 or higher)
	+ in the rStudio editor,  go to the menu :
		- Tools --> Install packages
	+ in the "packages" area, enter the following module names (separated by a space)
		- ggplot2 readr dplyr
	+ press the "install" button.

 * [git](https://github.com/) to retrieve the project from GitHub
```
$ sudo apt-get install git
```

[^1]: apper must also be installed, or use another installation program  

## Installation
***
(in progress)  
The project is composed of PYTHON scripts. You just have to install them from github, as well as the modules they use (see [Prerequisites](#prerequisites) ).  
As mentioned above, this project works in a Linux environment. you will have to adapt the OS commands to the target environment. And also, the paths and directories used must be modified if the scripts are executed under windows (replace the / characters in \\). see below.  

* get the scripts from github

in a linux console
from the local home directory (/home/xxxx)
```
$ git clone https://github.com/fcolasCTU/appCmax.git
$ cd appCmax
```

* adapt directory management to windows
	+ edit the setup.py script with idle
		- find the following command line
```:Python
	#=========================================
	# OS Name
	# Values LINUX
	#        WINDOWS
	#=========================================
	OS_Name = "LINUX"
```
		- Replace this with
```
	#=========================================
	# OS Name
	# Values LINUX
	#        WINDOWS
	#=========================================
	OS_Name = "WINDOWS"
```

## Usage
***
once the programs are retrieved from github,  
go to the **appCmax directory**  
Open the **script exeParam.py**  

### exeParam.py  

#### Description   
this one is divided into **two distinct parts**:  

#####  part \# 1.PARAMETERS TO BE MODIFIED  
which proposes a series of parameters assignment 
which will have an impact on the generation of the instances, 
and the name of the directory which will receive the final result.  

**Information about the test campaign :**
+ campaignName : Name of the campaign  
+ campaignUser : Name of the user  

  the directory of the final result ==>  
  ./Results/\[campaignName\]\_\[campaignUser\]_\[ddmmyyyy\] 
+ seedForce : None (see below)

**Information about the size n of the Pi sets (number of task sizes) :**  
Either with a start number and an end number.
+ N_NumberBegin: number of starting tasks
+ N_NumberEnd : number of ending tasks
e.g. if N_NumberBegin = 10 and N_NumberEnd=15, exeParam will create sets of 10 tasks, then 11 tasks, 12 tasks ... and finally 15 tasks.
These parameters are only used if N_List = \[\] (empty set)
On the other hand if N_List is filled, exeParam will use this parameter and will ignore N_NumberBegin and N_NumberEnd
+ N_List : List of task numbers
e.g. if N_List = \[10, 50, 100, 1000\], exeParam will generate 4 lists of tasks, one of 10 tasks, one of 50 tasks, one of 100 tasks and one of 1000 tasks.

**Information on the number of machines m :**  
(or processors) Works in the same way as the information on the size of the Pi sets.  
+ M_NumberBegin : number of starting machines
+ M_NumberEnd : number of ending machines
or 
+ M_List = \[m1, ....mj\]  
***Note***  
For each number of tasks, and number of machines parameterized, exeParam will create two sets of tasks. A "native" one with a requested number of tasks, and a completed one with m-1 tasks, which allows to control the optimal solution.
In the first case m set to calculate the average load per machine, in the second case, to build an instance of which we know the optimal solution.

**Instance generation information :**  
There are several ways to randomly generate lists of numbers. In particular by using statistical distributions (Uniform, Gamma, Beta, Exponential ...). 
These parameters ask how many of these lists of tasks should be generated according to the type of distribution desired:  
+ matUniformNumber: How many lists with a uniform distribution to generate
+ matNonUniformNumber : How many lists to generate with a non-uniform distribution
+ matGammaNumber : How many lists to generate with a Gamma distribution
+ matBetaNumber : How many lists to generate with a Beta distribution
+ matExponentialNumber : How many lists to generate with an Exponential distribution

**Use of real job logs (Parallel Worload Archive)**  
You can also use real logs, downloaded from the [Parallel Worload Archive site](https://www.cs.huji.ac.il/labs/parallel/workload/) (see below for downloading these files). In this case, the number of tasks is not controlled.  
+ matRealFiles = pwa.pwaFileChoice(X): How to work with the already downloaded files.  
	- if X = None, exeParam asks file by file, which one to use
	- if X = 0 : no file will be used
	- if X = 1: All files (present / already downloaded) will be used

**Distribution parameters :**  
+ nAb and nBb are used to generate lists using uniform and non-uniform distributions.  
For uniform instances, the tasks are uniformly distributed numbers in the range \[nAb ,nBb\].  
For non-uniform instances, 98% of the tasks are uniformly distributed numbers in the range \[0.9(nBb - nAb]), nBb\] and  
the rest uniformly distributed in the range \[nAb, 0.2(nBb - nAb)\].  
+ nAlpah : is used as a parameter of the Gamma and Beta distributions
+ nBeta: is used as a parameter of the Gamma distribution. (yes Gamma)
+ nLambda : is used as a parameter of the Exponential distribution.

**Which algorithms to use :**  
if 0, the algorithm is not used on the generated instances.  
1, the algorithm is used  
+ useLPT 1 or 0
+ useSLACK 1 or 0
+ useLDM 1 or 0
+ useCOMBINE 1 or 0
+ useMULTIFIT 1 or 0

#####  part \# 2. APPLICATION PART  

this part is application, and uses the parameters previously entered.

#### Execution  
It only remains to execute exeParam.py (F5 key if opened with IDLE)  
exeParam will   
+ generate all the requested instances.  
Note (seedForce):  
Each instance is generated at the same time as a seed. Each instance has its own seed. To regenerate the same instance, you have to change the value of seedForce (= None) with the seed number indicated in the result file.
+ Complete all native instances at m-1 tasks.  
+ Calculate indicators of these instances (means, variance, lower bound...)  
+ Run each chosen algorithm on each instance (native and completed), and enter the result found (Cmax)  
+ create the result directory  
+ generate a json file of the chosen parameters  
+ generate for each instance a task file  
+ generate the result file result.csv  
+ retrieve the r scripts (from the analysis directory) in this directory, execute them  on the result.csv file, and store, in this same directory, the result of the scripts (PDF for the graphs)  


### pwaRetrieve.py  
In the appCmax directory, the script pwaRetrieve.py allows to download job log files from real jobs, downloadable from the [Parallel Worload Archive site](https://www.cs.huji.ac.il/labs/parallel/workload/) .  

At runtime, pwaRetrieve asks how many files should be downloaded. pwaRetrieve stores them in compressed form in the **gz** directory, and decompresses them in the **log** directory.



