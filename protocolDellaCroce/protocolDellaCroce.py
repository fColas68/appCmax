import os.path
import pandas as pd

def main():

    fileMakespanCollumn = ['generateMethod','[a-b]','m','SLACK_vs_LPT_W','SLACK_vs_LPT_E','SLACK_vs_LPT_L','SLACK_vs_COMBINE_W','SLACK_vs_COMBINE_E','SLACK_vs_COMBINE_L','SLACK_vs_LDM_W','SLACK_vs_LDM_E','SLACK_vs_LDM_L']
    nCol1               = 0
    nCol2               = 1
    nCol3               = 2
    nSLACK_vs_LPT_W     = 3
    nSLACK_vs_LPT_E     = 4
    nSLACK_vs_LPT_L     = 5
    nSLACK_vs_COMBINE_W = 6
    nSLACK_vs_COMBINE_E = 7
    nSLACK_vs_COMBINE_L = 8
    nSLACK_vs_LDM_W     = 9
    nSLACK_vs_LDM_E     = 10
    nSLACK_vs_LDM_L     = 11

    # Dic for cumulate SUB CAMPAIGN
    #------------------------------------------
    resBySubCampaign = {}
    
    # Vaue item for resBySubCampaign
    #------------------------------------------
    content = ["","",0,0,0,0,0,0,0,0,0,0]

    # LIST and DICT for cumulate CAMPAIGN
    #------------------------------------------
    resByCampaign = {}
    campaign= ["","","",0,0,0,0,0,0,0,0,0]
    
    # ALL RESULTS 
    #------------------------------------------
    csvCampaigns = []   # stored in campaign rep
    csvAll = []         # stored in root folder (contain all total results for comparison
    
    # CAMPAIGN x ==============================================================
    listOfCampaigns = [f for f in os.listdir() if (os.path.isfile(f) == False)]
    for i in range(len(listOfCampaigns)):

        # RAZ LIST and Dictionnary resByCampaign
        camp = listOfCampaigns[i]
        campaign= [camp,"","",0,0,0,0,0,0,0,0,0]
        csvCampaigns = []
        
        # SUB CAMPAIGN PARTS =======================================
        listOfSubCampaign = [f for f in os.listdir(camp) if (os.path.isfile(f) == False)]
        for j in range(len(listOfSubCampaign)):
            
            # RAZ Dictionnary resBySubCampaign
            #------------------------------------------
            resBySubCampaign = {}

            # new rep
            #------------------------------------------
            rep = listOfSubCampaign[j]
            #print(rep)
        
            fileMakespan = camp+"/"+rep+"/rr_dellaCroce_m1_makespan.csv"
            fileTime     = camp+"/"+rep+"/rr_dellaCroce_m1_time.csv"

            # fileMakespan ============================
            if os.path.isfile(fileMakespan):

                cont = pd.read_csv(fileMakespan, usecols=fileMakespanCollumn, sep = '\t')
                #print(cont)
                for k in cont.index:
                    
                    # KEY of dictionnary generateMethod_[a-b]_m
                    #------------------------------------------
                    sid = cont['[a-b]'][k]
                    sgenerateMethod = cont['generateMethod'][k]
                    nM = cont['m'][k]
                    sM = str(nM).zfill(2)
                    key = sgenerateMethod+"_"+sid+"_"+sM
                    
                    #if key doesn't exists
                    #------------------------------------------
                    keyExists = resBySubCampaign.get(key)
                    if (not keyExists):resBySubCampaign[key] = [sgenerateMethod,sid, nM, 0,0,0,0,0,0,0,0,0]

                    #retrieve list of values
                    #------------------------------------------
                    content = resBySubCampaign[key]
                     
                    # cumulate SUB CAMPAIGN 
                    #------------------------------------------
                    content[nSLACK_vs_LPT_W]     += cont['SLACK_vs_LPT_W'][k]
                    content[nSLACK_vs_LPT_E]     += cont['SLACK_vs_LPT_E'][k]
                    content[nSLACK_vs_LPT_L]     += cont['SLACK_vs_LPT_L'][k]

                    content[nSLACK_vs_COMBINE_W] += cont['SLACK_vs_COMBINE_W'][k]
                    content[nSLACK_vs_COMBINE_E] += cont['SLACK_vs_COMBINE_E'][k]
                    content[nSLACK_vs_COMBINE_L] += cont['SLACK_vs_COMBINE_L'][k]

                    content[nSLACK_vs_LDM_W]     += cont['SLACK_vs_LDM_W'][k]
                    content[nSLACK_vs_LDM_E]     += cont['SLACK_vs_LDM_E'][k]
                    content[nSLACK_vs_LDM_L]     += cont['SLACK_vs_LDM_L'][k]

                    # cumulate CAMPAIGN 
                    #------------------------------------------
                    campaign[nSLACK_vs_LPT_W]     += content[nSLACK_vs_LPT_W]
                    campaign[nSLACK_vs_LPT_E]     += content[nSLACK_vs_LPT_E]
                    campaign[nSLACK_vs_LPT_L]     += content[nSLACK_vs_LPT_L]

                    campaign[nSLACK_vs_COMBINE_W] += content[nSLACK_vs_COMBINE_W]
                    campaign[nSLACK_vs_COMBINE_E] += content[nSLACK_vs_COMBINE_E]
                    campaign[nSLACK_vs_COMBINE_L] += content[nSLACK_vs_COMBINE_L]

                    campaign[nSLACK_vs_LDM_W]     += content[nSLACK_vs_LDM_W]
                    campaign[nSLACK_vs_LDM_E]     += content[nSLACK_vs_LDM_E]
                    campaign[nSLACK_vs_LDM_L]     += content[nSLACK_vs_LDM_L]
                    
                    # store the result content => resBySubCampaign
                    #------------------------------------------
                    resBySubCampaign[key] = content
                # END FOR K ==> SUB CAMPAIGN

                # Cumulate in the dc campaing result
                #------------------------------------------
                resByCampaign.update(resBySubCampaign)

            # END IF
        # END FOR J ==> CAMPAIGN

        # Transform Dic into LIST (for sort it)
        #------------------------------------------
        a = list(sorted(resByCampaign.items(), key=lambda t: t[0]))

        # Sort list by Key 
        #------------------------------------------
        s = sorted (a, key=lambda item: (item [0])) #, item [2]))

        # To store the value in csv List 
        #------------------------------------------
        for h in range(len(s)):
            t = s[h]
            csvCampaigns.append(t[1])
        # END FOR
        
        # cumlate Campain and total lists 
        #------------------------------------------
        csvCampaigns.append(campaign)   # for cumulative in detail file
        csvAll.append(campaign)         # for line in comparison results files
       
        # Store CAMPAING FILE 
        #------------------------------------------
        df = pd.DataFrame(csvCampaigns, columns=fileMakespanCollumn)
        df.to_csv(camp+"/res_dellaCroce_makesan_synth.csv")

    # END FOR I
    # Store CAMPAING FILE 
    #------------------------------------------
    dfAll = pd.DataFrame(csvAll, columns=fileMakespanCollumn)
    dfAll.to_csv("./res_dellaCroce_makesan_Comparison.csv")
    print("done.")

if __name__ == "__main__":
    main()
