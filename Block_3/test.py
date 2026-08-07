from sklearn.preprocessing import OneHotEncoder,LabelEncoder,StandardScaler,PolynomialFeatures
from sklearn.model_selection import train_test_split,cross_val_score
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestRegressor
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from xgboost import XGBRegressor
df=pd.read_csv("train.csv")
df_test=pd.read_csv("test.csv")
x_train=pd.get_dummies(df.drop(columns= [
    "Id",
    "player_id",
    "player_name",
    "match_id",
    "match_date",
    "player_rating"
    ,"performance_score"
]
),drop_first=True)

x_test=pd.get_dummies(df_test.drop(columns= [
    "Id",
    "player_id",
    "player_name",
    "match_id",
    "match_date"
    ,"performance_score"
]
),drop_first=True)
x_test = x_test.reindex(columns=x_train.columns, fill_value=0)
x_test["weighted_assists"]=x_test["assists"]-x_test["expected_assists_xa"]
x_test["weighted_goals"]=x_test["goals"]-x_test["expected_goals_xg"]
x_train["weighted_assists"]=x_train["assists"]-x_train["expected_assists_xa"]
x_train["weighted_goals"]=x_train["goals"]-x_train["expected_goals_xg"]
y_train=df["player_rating"]
model=RandomForestRegressor(n_estimators=400,random_state=42,max_depth=10) #This was the best model 
model.fit(x_train, y_train)
y_pred = model.predict(x_test)
csv_data=pd.DataFrame({"Id":df_test.iloc[x_test.index]["Id"],"Player Rating":y_pred})
csv_data.to_csv("result.csv",mode="a",header=True,index=False)