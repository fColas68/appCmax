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
itsefl | : | **in progress**
user's manual | : | **in progress**
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
$	sudo apt-get update
```

* [Python](https://www.python.org/): Version 3.4 
```
$	sudo apt-get install python3.4
$	sudo apt-get install python3.4-minimal
$	sudo apt-get install idle-python3.4 
```

* [pandas library](https://pandas.pydata.org/): Version 0.14.1-2
```
$	+ sudo apt-get install python3-pandas 
$	+ sudo apt-get install python3-pandas-lib
```

* [R Langage](https://cran.rstudio.com/): 3.5.3.1
```
$	+ sudo apt-get install r-base 
$	+ sudo apt-get install r-base-dev
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
$	sudo apt-get install git
```

[^1]: apper must also be installed, or use another installation program  

## Installation
***
(in progress)  
The project is composed of PYTHON scripts. You just have to install them from github, as well as the modules they use (see [Prerequisites](#prerequisites) ).  
As mentioned above, this project works in a Linux environment. you will have to adapt the OS commands to the target environment. And also, the paths and directories used must be modified if the scripts are executed under windows (replace the / characters in \\). see below.  

* get the scripts from github

in a linux console
from the local home directory (/hom```e/xxxx)
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
(in progress)  
open test.py with IDLE using Python 3, and run it.

## Collaboration
***
(in progress)  

