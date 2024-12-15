# Multiple Linear Regression

# Importing the libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import r2_score
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_squared_log_error
from sklearn.metrics import median_absolute_error
import statsmodels.regression.linear_model as lm
import pandas as pd
pd.options.display.max_columns=None


# Importing the dataset
dataset = pd.read_csv('aa.us.txt')
columnsTiltles = ["Date","Open","High","Low","Volume","Close"]
dataset = dataset.reindex(columns=columnsTiltles)
X = dataset.iloc[:, 1:-1].values
y = dataset.iloc[:, 5].values


'''# Encoding categorical data
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
labelencoder = LabelEncoder()
X[:, ] = labelencoder.fit_transform(X[:, ])
onehotencoder = OneHotEncoder(categorical_features = [])
X = onehotencoder.fit_transform(X).toarray()

# Avoiding the Dummy Variable Trap
X = X[:, 1:]'''

# Splitting the dataset into the Training set and Test set
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)

# Feature Scaling
from sklearn.preprocessing import StandardScaler
sc_X = StandardScaler()
X_train = sc_X.fit_transform(X_train)
X_test = sc_X.transform(X_test)

'''sc_y = StandardScaler()
y_train = sc_y.fit_transform(y_train)'''

# Fitting Multiple Linear Regression to the Training set
from sklearn.linear_model import LinearRegression
regressor = LinearRegression()
regressor.fit(X_train, y_train)

# Predicting the Test set results
y_pred = regressor.predict(X_test)


# Building the optimal model using Backward Elimination
import statsmodels.formula.api as sm
#Appending 1 to the matrix of feature X 
X = np.append(arr = np.ones((12074, 1)).astype(int), values = X, axis = 1)

#X_opt will be our optimal matrix which contains the attributes which are optimal
#/highly dependent.
X_opt = X[:, [0, 1, 2, 3, 4]]

#Regressor obj from OLS class , endog : dependent variable and exog = matrix of 
#features , as the intercept is not included, there we have to append 1

regressor_OLS = lm.OLS(endog = y, exog = X_opt).fit()
regressor_OLS.summary()
X_opt = X[:, [1, 2, 3, 4]]
regressor_OLS = lm.OLS(endog = y, exog = X_opt).fit()
regressor_OLS.summary()
X_opt = X[:, [1, 2, 3]]
regressor_OLS = lm.OLS(endog = y, exog = X_opt).fit()
regressor_OLS.summary()


# Splitting the dataset into the Training set and Test set
from sklearn.model_selection import train_test_split

X_train1, X_test1, y_train1, y_test1 = train_test_split(X_opt, y, test_size = 0.2, random_state = 0)

from sklearn.linear_model import LinearRegression
regressorr = LinearRegression()
regressorr.fit(X_train1, y_train1)


# Predicting the Test set results
y_pred1 = regressorr.predict(X_test1)

y_pred1_df=pd.DataFrame(y_pred1)
print(y_pred1_df)

plt.plot(y_test, y_pred)
plt.plot(y_test, y_pred1)

y_true = y_test.tolist()
y_pred2 = y_pred1.tolist()

y_pred2_df=pd.DataFrame(y_pred2)
y_true_df=pd.DataFrame(y_true)
print(y_true_df)
print(y_pred2_df)


r2_score(y_true, y_pred2)
print(r2_score(y_true, y_pred2))

mean_absolute_error(y_true, y_pred2)
print(mean_absolute_error(y_true, y_pred2))
mean_squared_error(y_true, y_pred2)
print(mean_squared_error(y_true, y_pred2))
mean_squared_log_error(y_true, y_pred2) 
print(mean_squared_log_error(y_true, y_pred2))
median_absolute_error(y_true, y_pred2)
print(median_absolute_error(y_true, y_pred2))


