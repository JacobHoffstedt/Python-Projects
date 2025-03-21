import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report, auc, precision_recall_curve
import matplotlib.pyplot as plt
import numpy as np
import joblib
import os
print("Script is running...")

df = pd.read_csv("")
print("Data loaded successfully!")
#print(df.head(20))
#print(df.info())
#print(df.isnull().sum())

x = df.drop(columns=["Class"]) #Predictors

y = df["Class"] #Outcome




print("Splitting into training and testing subsets")

#Splitting into training and test, 
#test_size: 20% used for testing, 80% for training, random_state:seed, stratify: balances outcomes in testing and training subsets.
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=1998, stratify=y) 
scaler = StandardScaler()
x_train_scaled = scaler.fit_transform(x_train)
x_test_scaled = scaler.transform(x_test)

#Converting back to dataframe
x_train_scaled = pd.DataFrame(x_train_scaled, columns =x_train.columns)
x_test_scaled = pd.DataFrame(x_test_scaled, columns =x_test.columns)
print("Scaled finished")

#Checking for highly correlated redundant features
corr_matrix = x_train_scaled.corr().abs()
upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k =1).astype(bool))
highly_correlated_features = [column for column in upper.columns if any(upper[column] > 0.9)]
print("The number of highly correlated features are", highly_correlated_features)
#Creating the model


if os.path.exists("logistic_regression_model.pkl"):
    print("Loading existing model...")
    model = joblib.load("logistic_regression_model.pkl")
else:
    print("Training the model...")
    model = LogisticRegression(solver = "saga", max_iter = 20000, verbose = 1)
    model.fit(x_train_scaled, y_train)
    joblib.dump(model, "logistic_regression_model.pkl")
    print("Training finished and model saved")



y_pred = model.predict(x_test_scaled)
y_prob = model.predict_proba(x_test_scaled)[:, 1]
print(y_pred)
print(y_prob)





print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))
precision, recall, _ = precision_recall_curve(y_test, y_prob)
auprc = auc(recall, precision)
print("AUPRC (Area Under Precision-Recall Curve):", auprc)

plt.figure(figsize=(8,6))
plt.plot(recall, precision, label=f"AUPRC = {auprc:.3f}")
plt.xlabel("Recall")
plt.ylabel("Precision")
plt.title("Precision-Recall Curve")
plt.legend()
plt.show()
print("End of run")