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
df=pd.read_csv("train.csv")

x=pd.get_dummies(df.drop(columns= [
    "Id",
    "player_id",
    "player_name",
    "match_id",
    "match_date",
    "player_rating"
]
),drop_first=True)
y=df["player_rating"]
x_train,x_test,y_train,y_test=train_test_split(x,y,random_state=42,test_size=0.2)
model=RandomForestRegressor(n_estimators=200,random_state=42,max_depth=7)
model.fit(x_train, y_train)
y_pred = model.predict(x_test)
print(mean_squared_error(y_pred,y_test))
