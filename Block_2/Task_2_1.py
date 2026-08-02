import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


results=pd.read_csv("results.csv")
def decade_map(date):
    year=int(date.split("-")[0]) 
    return year//10 
results["decade"]=results["date"].map(decade_map)
results["draw"]=results["home_score"]==results["away_score"]
results["Winning margin"]=abs(results["home_score"]-results["away_score"])
results["goals"]=results["home_score"]+results["away_score"]
print(results.groupby("decade")[["draw","Winning margin","goals"]].mean())
