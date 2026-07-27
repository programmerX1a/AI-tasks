def process_match(standings,team1,team2,score1,score2):
    standings[team1]["P"]+=1
    standings[team2]["P"]+=1
    standings[team1]["GF"]=standings[team1]["GF"]+score1
    standings[team1]["GA"]=standings[team1]["GA"]+score2
    standings[team2]["GF"]=standings[team2]["GF"]+score2
    standings[team2]["GA"]=standings[team2]["GA"]+score1
    gd1=standings[team1]["GF"]-standings[team1]["GA"]
    gd2=standings[team2]["GF"]-standings[team2]["GA"]
    standings[team1]["GD"]=f"+{gd1}" if gd1>0 else f"{gd1}"
    standings[team2]["GD"]=f"+{gd2}" if gd2>0 else f"{gd2}"

    if score1>score2:
        standings[team1]["W"]+=1
        standings[team2]["L"]+=1
        standings[team1]["Pts"]+=3
    elif score1<score2:
        standings[team1]["L"]+=1
        standings[team2]["W"]+=1
        standings[team2]["Pts"]+=3
    else:
        standings[team1]["D"]+=1
        standings[team2]["D"]+=1
        standings[team1]["Pts"]+=1
        standings[team2]["Pts"]+=1
    return standings

  
def print_standings(standings):
    sorted_standings=[i for i in standings]
    for i in range(len(sorted_standings)):
        for j in range(i+1,len(sorted_standings)):
            team1=sorted_standings[i]
            team2=sorted_standings[j]
            if(standings[team1]["Pts"]<standings[team2]["Pts"]):
                temp=sorted_standings[i]
                sorted_standings[i]=sorted_standings[j]
                sorted_standings[j]=temp
            elif(standings[team1]["Pts"]==standings[team2]["Pts"]):
                if(standings[team1]["GF"]-standings[team1]["GA"]<standings[team2]["GF"]-standings[team2]["GA"]):
                    temp=sorted_standings[i]
                    sorted_standings[i]=sorted_standings[j]
                    sorted_standings[j]=temp
                elif(standings[team1]["GF"]-standings[team1]["GA"]==standings[team2]["GF"]-standings[team2]["GA"]):
                    if(standings[team1]["GF"]+standings[team1]["GA"]<standings[team2]["GF"]-standings[team2]["GA"]):
                        temp=sorted_standings[i]
                        sorted_standings[i]=sorted_standings[j]
                        sorted_standings[j]=temp
    print("Team",end="  ")
    keys=[]
    for i in standings["ARG"].keys():
        keys.append(i)
        print(i,end="  ")
    print("",end="\n")
    for i in sorted_standings:
        print(f"{i}",end="   ")
        m=0
        for j in standings[i].values():
            print(j,end=" "*(len(keys[m])+1) )
            m+=1
        print("",end='\n')
           

                


            


   




                







if(__name__=="__main__"):
    teams=["ARG","MEX","POL","KSA"]
    standings={}
    for i in teams:
        standings[i]={"P":0,"W":0,"D":0,"L":0,"GF":0,"GA":0,"GD":0,"Pts":0}
    for i in range(0,len(teams)):
        for j in range(i+1,len(teams)):
            while True:
                try:
                    match=input(f"Enter score for {teams[i]} vs {teams[j]} (format: 2-0):")
                    score=match.split("-")
                    if len(score)!=2:
                        raise Exception
                    score1=int(score[0])
                    score2=int(score[1])
                    standings=process_match(standings,teams[i],teams[j],score1,score2)                          
                    break
                except ValueError:
                    print("Enter the correct format")
    print_standings(standings)        





                
         


    
        
    
    