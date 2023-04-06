import pandas as pd
data = pd.read_csv('Sales.csv')


data.info()
print(data.isnull().sum())
data = data.fillna(data.mean())
print(data.corr())

data = data.replace('Mega', 0)
data = data.replace('Micro', 1)
data = data.replace('Nano', 2)
data = data.replace('Macro', 3)

x = data.iloc[:, :-1].values
y = data.iloc[:, -1].values

from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x,y, test_size=0.20, random_state=0)

from sklearn.metrics import r2_score, mean_squared_error as mse
from sklearn.ensemble import RandomForestRegressor
rf_regressor = RandomForestRegressor()
rf_regressor.fit(x_train, y_train)

y_pred = rf_regressor.predict(x_test)

#%%
print(r2_score(y_test, y_pred))
print(mse(y_test, y_pred)**0.5)
print(rf_regressor.predict([[78.0, 24.9,4.2,3.0]]))

#%%
import pickle

pickle.dump(rf_regressor,open('model.pkl','wb'))
