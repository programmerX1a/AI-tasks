from sklearn.preprocessing import OneHotEncoder,LabelEncoder,StandardScaler,PolynomialFeatures
from sklearn.model_selection import train_test_split,cross_val_score
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestRegressor
import xgboost as xgb
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
df=pd.read_csv("train.csv")
df["weighted_goals"]=df["goals"]-df["expected_goals_xg"]
df["weighted_assists"]=df["assists"]-df["expected_assists_xa"]
important_attributes=df.columns[23:].drop(["performance_score","player_rating"])
attack_attributes=important_attributes.drop(["successful_crosses","penalty_saves","punches","save_percentage","saves","clean_sheet","goals_conceded"])
midfielder_attributes=important_attributes.drop(["penalty_saves","punches","save_percentage","saves","clean_sheet","goals_conceded"])
goalkeeper_attributes=important_attributes.drop(["expected_goals_xg","goals","shots","shots_on_target","blocks","tackles","successful_crosses","expected_assists_xa","total_assists_tournament","weighted_goals","weighted_assists"])
defender_attributes=important_attributes.drop(["penalty_saves","punches","save_percentage","saves","clean_sheet","goals_conceded"])
df_test=pd.read_csv("test.csv")
df_test["weighted_goals"]=df_test["goals"]-df_test["expected_goals_xg"]
df_test["weighted_assists"]=df_test["assists"]-df_test["expected_assists_xa"]
attributes={
    "Goalkeeper":goalkeeper_attributes,
    "Midfielder":midfielder_attributes,
    "Forward":attack_attributes,
    "Defender":defender_attributes
}

flag=True
for i in df["position"].values.unique():
    df_modified=df[df["position"]==i]
    df_test_modified=df_test[df_test["position"]==i]
    x_train=pd.get_dummies(df_modified[attributes[i]],drop_first=True)
    y_train=df_modified["player_rating"]
    x_test=pd.get_dummies(df_test_modified[attributes[i]],drop_first=True)
    model=RandomForestRegressor(n_estimators=200,random_state=42,max_depth=7)
    model.fit(x_train, y_train)
    y_pred = model.predict(x_test)
    csv_data=pd.DataFrame({"Id":df_test.iloc[x_test.index]["Id"],"Player Rating":y_pred})
    csv_data.to_csv("result.csv",mode="a",index=False,header=flag)
    flag=False
    print(mean_squared_error(y_pred,y_test))
