from Task_1_3 import *
import os
import json
from google import genai #pip install google-genai 
from dotenv import load_dotenv
load_dotenv("api.env")
class MatchAI:
    def __init__(self,model,controlled_team,risk_tolerance):
        self.model=model
        self.controlled_team=controlled_team
        self.risk_tolerance=risk_tolerance
        self.decision_log=[]
    def observe_state(self,match):
        minute=match.current_minute
        opponent=match.away_team if match.home_team==self.controlled_team else match.home_team
        active_team=""
        for i in self.controlled_team.active_lineup:
            active_team+=i.name+","
        attack=self.controlled_team.get_aggregate_attack()
        defence=self.controlled_team.get_aggregate_defence()
        opponent_attack=opponent.get_aggregate_attack()
        opponent_defence=opponent.get_aggregate_defence()
        bench=""
        for i in self.controlled_team.bench:
            bench+=i.name+","
        return f"You are coaching {self.controlled_team} against {opponent.country_name} in a football match. Current minute is {minute}. Your active players are {active_team}. Your reserve players are {bench}. Your team's aggregate attack is {attack} and aggregate defence is {defence}. The opponent's aggregate attack is {opponent_attack} and aggregate defence is {opponent_defence}. You are required to make one of the following decisions with risk tolerance: {self.risk_tolerance}.Return me a JSON file where you store the decision in \"decision\" key and return one of them: (SUBSTITUTE,CHANGE_FORMATION,HOLD,PUSH_ATTACK) and store a detailed response on why you chose that decision in a \"explaination\" key Also very important to return me ONLY the JSON file so i can parse it aka no Here's the JSON File: ."
    def decide_action(self,match):
        client = genai.Client( api_key=os.getenv("API_KEY"))
        response=client.models.generate_content(model=self.model,contents=self.observe_state(match))
        json_response=json.loads(response.text)
        self.decision_log.append(json_response["explaination"])
        return json_response["decision"]
    def apply_decision(self,decision,match):
        if decision=="SUBSTITUTE":
            lowest_stamina=100
            for i in self.controlled_team.active_lineup:
                if i.stamina<lowest_stamina:
                    lowest_stamina=i.stamina
                    player_out=i
            highest_stamina=0
            for i in self.controlled_team.bench:
                if i.stamina>highest_stamina:
                    highest_stamina=i.stamina
                    player_in=i
            self.controlled_team.execute_substitution(player_out,player_in)
        elif decision=="CHANGE_FORMATION":
            ratio=self.controlled_team.get_aggregate_attack()/self.controlled_team.get_aggregate_defence()
            if ratio>1:
                for i in self.controlled_team.active_lineup:
                    if i.position==Position.FORWARD:
                        player_atk=i
                    if i.position==Position.DEFENDER: 
                        player_def=i
                player_atk.position=Position.DEFENDER
                player_def.position=Position.FORWARD

            else:
                for i in self.controlled_team.active_lineup:
                    if i.position==Position.DEFENDER:
                        player_def=i
                    if i.position==Position.FORWARD: 
                        player_atk=i
                player_def.position=Position.FORWARD
                player_atk.position=Position.DEFENDER
        elif decision=="HOLD":
            self.controlled_team.risk_tolerance-=0.2
            for i in self.controlled_team.active_lineup:
                i.risk_tolerance-=0.2
        elif decision=="PUSH_ATTACK":
            self.controlled_team.risk_tolerance+=0.2
            for i in self.controlled_team.active_lineup:
                i.risk_tolerance+=0.2  
        
     

                
        




    
        
        
        




        
   


if __name__ == "__main__":
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
    match_ai = MatchAI("gemini-3.6-flash", ARG, 0.7) #Controlling Argentina with gemini 3.6-flash model 
    match=Match(ARG,ES,0,1,6,[],Phase.REGULATION) #Argentina vs Spain,0-1 Minute 6
    action=match_ai.decide_action(match)
    print(action)
    match_ai.apply_decision(match, action)
    print(match_ai.decision_log[0])
    
    


