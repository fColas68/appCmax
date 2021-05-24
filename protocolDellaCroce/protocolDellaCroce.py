import os.path
import pandas

def main():
    campaignDellaCroce = "cumulDC"


    fileMakespanCollumn = ['generateMethod','[a-b]','m','SLACK_vs_LPT_W','SLACK_vs_LPT_E','SLACK_vs_LPT_L','SLACK_vs_COMBINE_W','SLACK_vs_COMBINE_E','SLACK_vs_COMBINE_L','SLACK_vs_LDM_W','SLACK_vs_LDM_E','SLACK_vs_LDM_L']
    nSLACK_vs_LPT_W     = 3
    nSLACK_vs_LPT_E     = 4
    nSLACK_vs_LPT_L     = 5
    nSLACK_vs_COMBINE_W = 6
    nSLACK_vs_COMBINE_E = 7
    nSLACK_vs_COMBINE_L = 8
    nSLACK_vs_LDM_W     = 9
    nSLACK_vs_LDM_E     = 10
    nSLACK_vs_LDM_L     = 11
    resBySubCampaign = {}
    content = ["","",0,0,0,0,0,0,0,0,0,0]

    resByCampaign = {}

    # CAMPAIGN x ==============================================================
    listOfCampaigns = [f for f in os.listdir() if (os.path.isfile(f) == False)]
    for i in range(len(listOfCampaigns)):
        
        camp = listOfCampaigns[i]
        #print(camp)
        
        # subDirectories Campaign parts =======================================
        listOfSubCampaign = [f for f in os.listdir(camp) if (os.path.isfile(f) == False)]
        for j in range(len(listOfSubCampaign)):
            
            # RAZ Dictionnary resByCampaign
            resBySubCampaign = {}

            # new rep
            rep = listOfSubCampaign[j]
            #print(rep)
        
            fileMakespan = camp+"/"+rep+"/res_dellaCroce_makesan.csv"
            fileTime     = camp+"/"+rep+"/res_dellaCroce_time.csv"

            # fileMakespan ============================
            if os.path.isfile(fileMakespan):

                cont = pandas.read_csv(fileMakespan, usecols=fileMakespanCollumn, sep = '\t')
                #print(cont)
                for k in cont.index:
                    
                    
                    sid = cont['[a-b]'][k]
                    sgenerateMethod = cont['generateMethod'][k]
                    nM = cont['m'][k]
                    sM = str(nM).zfill(2)
                    key = sgenerateMethod+"_"+sid+"_"+sM
                    #key = [sgenerateMethod,sid,sM]
                    #if key doesn't exists
                    keyExists = resBySubCampaign.get(key)
                    if (not keyExists):resBySubCampaign[key] = [sgenerateMethod,sid, nM, 0,0,0,0,0,0,0,0,0]

                    #retrieve list of values
                    content = resBySubCampaign[key]
                     
                    # cumulative 
                    content[nSLACK_vs_LPT_W]     += cont['SLACK_vs_LPT_W'][k]
                    content[nSLACK_vs_LPT_E]     += cont['SLACK_vs_LPT_E'][k]
                    content[nSLACK_vs_LPT_L]     += cont['SLACK_vs_LPT_L'][k]

                    content[nSLACK_vs_COMBINE_W] += cont['SLACK_vs_COMBINE_W'][k]
                    content[nSLACK_vs_COMBINE_E] += cont['SLACK_vs_COMBINE_E'][k]
                    content[nSLACK_vs_COMBINE_L] += cont['SLACK_vs_COMBINE_L'][k]

                    content[nSLACK_vs_LDM_W]     += cont['SLACK_vs_LDM_W'][k]
                    content[nSLACK_vs_LDM_E]     += cont['SLACK_vs_LDM_E'][k]
                    content[nSLACK_vs_LDM_L]     += cont['SLACK_vs_LDM_L'][k]
                    
                    # store the result
                    resBySubCampaign[key] = content
                    
                    
                # END FOR K
                resByCampaign.update(resBySubCampaign)
            # END IF
        # END FOR J
        a = list(sorted(resByCampaign.items(), key=lambda t: t[0]))
        print(a)
 #       for cle,valeur in resByCampaign.items():
 #           print(cle, valeur)
       

    # END FOR I

if __name__ == "__main__":
    main()
