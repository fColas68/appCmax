import os.path
import pandas

def main():
    campaignDellaCroce = "cumulDC"

    idCurrent = 0
    listOfDirectories = [f for f in os.listdir() if (os.path.isfile(f) == False)]
    for i in range(len(listOfDirectories)):
        rep = listOfDirectories[i]
        file = rep+"/result.csv"
        if os.path.isfile(file):
            cont = pandas.read_csv(file, usecols=['generateMethode','id','n','[a-b]','m1_n','m1Optimal','resultConcerns','algoName','makespan','time'])
            #for i in range(len(cont)):
            #    print(cont[i])
            for i in cont.index:
                id = cont['id'][i]
                
                if (idCurrent == 0): idCurrent = id
                if idCurrent != id:
                    setRup(idCurrent)
                    idCurrent = id
            # END FOR
            setRup(idCurrent)
        # END IF
    # END FOR     


def setRup(nID):
    print(nID)

if __name__ == "__main__":
    main()
