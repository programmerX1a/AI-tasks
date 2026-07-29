from enum import Enum
import random
class Position(Enum):
    GOALKEEPER="GOALKEEPER"
    MIDFIELDER="MIDFIELDER"
    DEFENDER="DEFENDER"
    FORWARD="FORWARD"





class Player:
    def __init__(self,name,position,base_attack,base_defence):
        self.name=name
        self.risk_tolerance=0.5
        try:
            self.position=Position(position)
        except:
            print("Position doesnt exist assigning it to Attacker")
            self.position=Position("FORWARD")
        if base_attack<1:
            self.base_attack=1
        elif base_attack>100:
            self.base_attack=100
        else:
            self.base_attack=base_attack
        if base_defence<1:
            self.base_defence=1
        elif base_defence>100:
            self.base_defence=100
        else:
            self.base_defence=base_defence
        self.stamina=100.0
    def deplete_stamina(self,rate):
        self.stamina-=rate*(1+(self.risk_tolerance-0.5)*0.4)
        if self.stamina<10:
            self.stamina=10
    def get_effective_attack(self):
        return self.base_attack*(self.stamina/100.0)
    def get_effective_defence(self):
        return self.base_defence*(self.stamina/100.0)
    
class Team:
    def __init__(self,country_name,roster,active_lineup):
        self.risk_tolerance=0.5
        self.bench=[]
        self.country_name=country_name
        self.roster=roster
        self.active_lineup=active_lineup
        for i in roster:
            if i not in self.active_lineup:
                self.bench.append(i)
        self.substitution_remaining=5
    def get_aggregate_attack(self):
        count=0
        sum=0
        for i in self.active_lineup:
            if i.position==Position.MIDFIELDER or i.position==Position.FORWARD:
                count+=1
                sum+=i.get_effective_attack()
        return sum/count
    def get_aggregate_defence(self):
        count=0
        sum=0
        for i in self.active_lineup:
            if i.position==Position.DEFENDER or i.position==Position.GOALKEEPER:
                count+=1
                sum+=i.get_effective_defence()
        return sum/count
    def execute_substitution(self,player_out,player_in):
        if self.substitution_remaining>0:
            self.active_lineup.remove(player_out)
            self.bench.append(player_out)
            self.bench.remove(player_in)
            self.active_lineup.append(player_in)
            self.substitution_remaining-=1
            print(f"{player_out.name} is now in place of {player_in.name}")
        else:
            print("You can't substitute anymore")
    


class EventType(Enum):
    GOAL="GOAL"
    SUBSTITUTION="SUBSTITUTION"
    HALF_TIME="HALF_TIME"  
    FULL_TIME="FULL_TIME"
    RED_CARD="RED_CARD"
class MatchEvent:
    def __init__(self,event_id,event_type,minute,team,player,outcome_text):
        self.event_id=event_id
        try:
            self.event_type=EventType(event_type)
        except:
            print("Event type doesnt exist assigning it to GOAL")
            self.event_type=EventType("GOAL")
        self.minute=minute
        self.team=team
        self.player=player
        self.outcome_text=outcome_text
    def to_string(self):
        if self.event_type==EventType.HALF_TIME or self.event_type==EventType.FULL_TIME:
            return f"Reached {self.event_type.value} at {self.minute}th minute Outcome Text:{self.outcome_text}"
        elif self.event_type==EventType.SUBSTITUTION:
            return f"{self.event_type.value} by {self.player.name} from {self.team.country_name} at {self.minute}th minute Outcome Text:{self.outcome_text}"
        else:
            return f"{self.event_type.value} by {self.player.name} from {self.team.country_name} at {self.minute}th minute Outcome Text:{self.outcome_text}"
    
class Phase(Enum):
    REGULATION="REGULATION"
    FINISHED="FINISHED"
    PENALTIES="PENALTIES"


class Match:
    def __init__(self,home_team,away_team,home_score,away_score,current_minute,timeline,phase):
        self.home_team=home_team
        self.away_team=away_team
        self.home_score=home_score
        self.away_score=away_score
        self.current_minute=current_minute
        self.timeline=timeline
        try:
            self.phase=Phase(phase)
        except:
            print("Phase doesnt exist. Set to REGULATION")
            self.phase=Phase("REGULATION")
    def process_goal_attempt(self,attacking_team,defending_team):
        attempt=random.randint(1,100)
        if attempt<=10:
            attack=attacking_team.get_aggregate_attack()
            defence=defending_team.get_aggregate_defence()
            if attack*random.uniform(0.75,1.25+(attacking_team.risk_tolerance-0.5)*0.4)>defence*1.3*random.uniform(0.8,1.20):
                self.timeline.append(MatchEvent(len(self.timeline),EventType.GOAL,self.current_minute,attacking_team,attacking_team.active_lineup[random.randint(0,len(attacking_team.active_lineup)-1)],f"{attacking_team.country_name} score a goal against {defending_team.country_name}"))
                if attacking_team==self.home_team:
                    self.home_score+=1
                else:
                    self.away_score+=1

    def run_minute_tick(self):
        self.current_minute+=1
        for i in self.home_team.active_lineup:
            i.deplete_stamina(0.5)
        for i in self.away_team.active_lineup:
            i.deplete_stamina(0.5)
        if random.randint(1,100)>=50:  
            self.process_goal_attempt(self.home_team,self.away_team)
        else:
            self.process_goal_attempt(self.away_team,self.home_team)

        for i in self.home_team.active_lineup:
            if i.stamina<30:
                player_in=random.randint(0,len(self.home_team.bench)-1)
                self.home_team.execute_substitution(i,self.home_team.bench[player_in])
                self.time_line.append(MatchEvent(len(self.timeline),EventType.SUBSTITUTION,self.current_minute,self.home_team,i,f"{self.home_team.country_name} substituted {i.name} with {player_in}"))
        for i in self.away_team.active_lineup:
            if i.stamina<30:
                player_in=random.randint(0,len(self.away_team.bench)-1)
                self.away_team.execute_substitution(i,self.away_team.bench[player_in])
                self.timeline.append(MatchEvent(len(self.timeline),EventType.SUBSTITUTION,self.current_minute,self.away_team,i,f"{self.away_team.country_name} substituted {i.name} with {player_in}"))
        if random.randint(1,1000)<=2: #0.2% chance of an incident worthy of a red card
            if random.randint(1,100)>=50:
                player_idx=random.randint(0,len(self.home_team.active_lineup)-1)
                player=self.home_team.active_lineup[player_idx]
                self.home_team.active_lineup.remove(self.home_team.active_lineup[player_idx])
                self.timeline.append(MatchEvent(len(self.timeline),EventType.RED_CARD,self.current_minute,self.home_team,player,f"{self.home_team.country_name} player {player.name} received a red card"))
            else:
                player_idx=random.randint(0,len(self.away_team.active_lineup)-1)
                player=self.away_team.active_lineup[player_idx]
                self.away_team.active_lineup.remove(self.away_team.active_lineup[player_idx])
                self.timeline.append(MatchEvent(len(self.timeline),EventType.RED_CARD,self.current_minute,self.away_team,player,f"{self.away_team.country_name} player {player.name} received a red card"))
        
 
        if self.current_minute==45:
            self.timeline.append(MatchEvent(len(self.timeline),EventType.HALF_TIME,self.current_minute,None,None,"Half time"))
        elif self.current_minute==90:
            self.timeline.append(MatchEvent(len(self.timeline),EventType.FULL_TIME,self.current_minute,None,None,"Full time"))
            if self.home_score!=self.away_score:
                self.phase=Phase.FINISHED
            else:
                self.phase=Phase.PENALTIES
            
        






if __name__=="__main__":
    argentina_roster = [
    Player("Emiliano Martínez", Position.GOALKEEPER, 15, 98),
    Player("Gerónimo Rulli", Position.GOALKEEPER, 15, 88),
    Player("Walter Benítez", Position.GOALKEEPER, 15, 85),
    Player("Cristian Romero", Position.DEFENDER, 60, 94),
    Player("Nicolás Otamendi", Position.DEFENDER, 58, 90),
    Player("Lisandro Martínez", Position.DEFENDER, 65, 92),
    Player("Germán Pezzella", Position.DEFENDER, 55, 86),
    Player("Nahuel Molina", Position.DEFENDER, 72, 88),
    Player("Gonzalo Montiel", Position.DEFENDER, 68, 85),
    Player("Nicolás Tagliafico", Position.DEFENDER, 68, 87),
    Player("Valentín Barco", Position.DEFENDER, 75, 80),
    Player("Enzo Fernández", Position.MIDFIELDER, 82, 86),
    Player("Alexis Mac Allister", Position.MIDFIELDER, 84, 82),
    Player("Rodrigo De Paul", Position.MIDFIELDER, 80, 84),
    Player("Leandro Paredes", Position.MIDFIELDER, 76, 86),
    Player("Exequiel Palacios", Position.MIDFIELDER, 79, 82),
    Player("Giovani Lo Celso", Position.MIDFIELDER, 84, 74),
    Player("Thiago Almada", Position.MIDFIELDER, 87, 68),
    Player("Lionel Messi", Position.FORWARD, 98, 60),
    Player("Julián Álvarez", Position.FORWARD, 90, 72),
    Player("Lautaro Martínez", Position.FORWARD, 91, 68),
    Player("Ángel Correa", Position.FORWARD, 86, 65),
    Player("Alejandro Garnacho", Position.FORWARD, 91, 60),
    Player("Nicolás González", Position.FORWARD, 84, 72),
    Player("Paulo Dybala", Position.FORWARD, 89, 60),
    Player("Valentín Carboni", Position.FORWARD, 83, 64),
]

    argentina_active_lineup = [
        argentina_roster[0],  
        argentina_roster[4],   
        argentina_roster[3],  
        argentina_roster[7],   
        argentina_roster[9],   
        argentina_roster[11], 
        argentina_roster[12],  
        argentina_roster[13], 
        argentina_roster[18],  
        argentina_roster[19],  
        argentina_roster[20],  
    ]

    spain_roster = [
        Player("Unai Simón", Position.GOALKEEPER, 15, 96),
        Player("David Raya", Position.GOALKEEPER, 15, 91),
        Player("Álex Remiro", Position.GOALKEEPER, 15, 89),
        Player("Dani Carvajal", Position.DEFENDER, 75, 92),
        Player("Jesús Navas", Position.DEFENDER, 70, 84),
        Player("Robin Le Normand", Position.DEFENDER, 60, 91),
        Player("Aymeric Laporte", Position.DEFENDER, 62, 90),
        Player("Pau Cubarsí", Position.DEFENDER, 65, 89),
        Player("Dani Vivian", Position.DEFENDER, 60, 88),
        Player("Marc Cucurella", Position.DEFENDER, 74, 88),
        Player("Alejandro Grimaldo", Position.DEFENDER, 82, 84),
        Player("Rodri", Position.MIDFIELDER, 86, 96),
        Player("Pedri", Position.MIDFIELDER, 88, 82),
        Player("Fabián Ruiz", Position.MIDFIELDER, 84, 84),
        Player("Martín Zubimendi", Position.MIDFIELDER, 76, 90),
        Player("Dani Olmo", Position.MIDFIELDER, 90, 72),
        Player("Mikel Merino", Position.MIDFIELDER, 82, 86),
        Player("Álex Baena", Position.MIDFIELDER, 86, 70),
        Player("Lamine Yamal", Position.FORWARD, 95, 65),
        Player("Nico Williams", Position.FORWARD, 92, 67),
        Player("Álvaro Morata", Position.FORWARD, 88, 70),
        Player("Mikel Oyarzabal", Position.FORWARD, 87, 72),
        Player("Ferran Torres", Position.FORWARD, 86, 68),
        Player("Yeremy Pino", Position.FORWARD, 85, 68),
        Player("Ayoze Pérez", Position.FORWARD, 84, 70),
        Player("Fermín López", Position.MIDFIELDER, 87, 72),
    ]

    spain_active_lineup = [
        spain_roster[0],  
        spain_roster[3],   
        spain_roster[5],   
        spain_roster[6],  
        spain_roster[9],  
        spain_roster[11], 
        spain_roster[12],  
        spain_roster[13], 
        spain_roster[18],  
        spain_roster[19],  
        spain_roster[20],  
    ]
 
    ARG=Team("Argentina",argentina_roster,argentina_active_lineup)
    ES=Team("Spain",spain_roster,spain_active_lineup)
    match=Match(ARG,ES,0,0,0,[],Phase.REGULATION)
    for i in range(0,91):
        match.run_minute_tick()

    for i in match.timeline:
        print(i.to_string())

    if match.phase==Phase.PENALTIES:
        home_penalty=0
        away_penalty=0
        print(f"Score: {match.home_team.country_name}:{match.home_score} {match.away_team.country_name}:{match.away_score}\nTeams are in penalty phase.") 
        for i in range(0,5):     
            while(True):
                try:
                    team1=int(input(f"{match.home_team.country_name}:{home_penalty} {match.away_team.country_name}:{away_penalty} {match.home_team.country_name} Turn ( format: 1(Score) 0(Miss) ):"))
                    home_penalty+=team1
                    team2=int(input(f"{match.home_team.country_name}:{home_penalty} {match.away_team.country_name}:{away_penalty} {match.away_team.country_name} Turn ( format: 1(Score) 0(Miss) ):"))
                    away_penalty+=team2
                    break
                except ValueError:
                    print("Invalid input. Please enter 1 for score or 0 for miss.")
        while home_penalty==away_penalty:
            print("Sudden Death")
            while(True):
                try:
                    team1=int(input(f"{match.home_team.country_name}:{home_penalty} {match.away_team.country_name}:{away_penalty} {match.home_team.country_name} Turn ( format: 1(Score) 0(Miss) ):"))
                    if team1!=1 and team1!=0:
                        print("Enter 1 for score or 0 for miss")
                        continue
                    home_penalty+=team1
                    team2=int(input(f"{match.home_team.country_name}:{home_penalty} {match.away_team.country_name}:{away_penalty} {match.away_team.country_name} Turn ( format: 1(Score) 0(Miss) ):"))
                    if team2!=1 and team2!=0:
                        print("Enter 1 for score or 0 for miss")
                        continue
                    away_penalty+=team2
                    break
                except ValueError:
                    print("Invalid input. Please enter 1 for score or 0 for miss.")

        print(f"Score:{match.home_team.country_name}:{match.home_score} {match.away_team.country_name}:{match.away_score}\n Penalties: {match.home_team.country_name}:{home_penalty} {match.away_team.country_name}:{away_penalty}")    
    elif match.phase==Phase.FINISHED:
        print(f"Score:{match.home_team.country_name}:{match.home_score}   {match.away_team.country_name}:{match.away_score} ")




    