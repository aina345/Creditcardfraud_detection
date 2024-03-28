# -*- coding: utf-8 -*-
"""creditcard.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1zngftBThace5-4uuFWi1JxKXtFHHzRzs
"""

# Define necessary libraries for the project
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler
from sklearn.impute import SimpleImputer  # Import SimpleImputer for handling missing values
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix, recall_score
import warnings

# Import the dataset
data = pd.read_csv('creditcard.csv')

# Check the description and information of data
data.describe()
data.info()

# Calculate the correlation matrix
sample_corr = data.corr(numeric_only=True)[['Amount', 'Class']]
sample_corr

# Plot a heatmap to visualize feature correlations
plt.figure(figsize=(8, 7))
sns.heatmap(data=sample_corr.sort_values(['Amount', 'Class'], ascending=False), annot=True, cmap='Oranges')
plt.tight_layout()

# Define the function to show feature correlation
def show_feature_corr(data: pd.DataFrame, x: str, y: str, figsize: tuple = (6, 3)):
    plt.figure(figsize=figsize)
    sns.scatterplot(data=data, x=x, y=y, hue='Class')
    plt.tight_layout()

# Visualize feature correlation data using a scatter plot
show_feature_corr(data, 'V7', 'Amount')

# Visualize the class distribution
plt.figure(figsize=(17, 6))
data['Class'].value_counts().plot(kind='pie', autopct='%0.2f%%', ylabel='', title='Class')
data['Class'].value_counts()

# Display the segmentation of the class

# Split the data into train and test
from sklearn.model_selection import train_test_split
x = data.drop(['Class'], axis=1)
y = data['Class']
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25, random_state=42)
x_train[:5]

# Handle missing values with SimpleImputer
imputer = SimpleImputer(strategy='mean')  # You can choose a different strategy if needed
x_train = imputer.fit_transform(x_train)
x_test = imputer.transform(x_test)

# Check for missing values in y_test
missing_y_test = y_test.isnull().sum()

if missing_y_test > 0:
    # Handle missing values in y_test, for example, by dropping rows with missing labels
    print(f"Found {missing_y_test} missing values in y_test. Dropping rows with missing labels.")

    # Get the indices of non-missing values in y_test
    valid_indices = ~y_test.isnull()

    # Update y_test and x_test to keep only valid data
    y_test = y_test[valid_indices]
    x_test = x_test[valid_indices]

# Scale the data with MinMaxScaler
from sklearn.preprocessing import MinMaxScaler
msc = MinMaxScaler()
x_train = msc.fit_transform(x_train)
x_test = msc.transform(x_test)

# Define and fit the Logistic Regression model
lr = LogisticRegression()
lr.fit(x_train, y_train)
yhat_lr = lr.predict(x_test)

# Calculate and display the metrics for Logistic Regression
from sklearn.metrics import accuracy_score, recall_score, precision_score, f1_score
from sklearn.metrics import confusion_matrix

# Calculate the metrics
accuracy_lr = accuracy_score(y_test, yhat_lr)
recall_lr = recall_score(y_test, yhat_lr, average='micro')
precision_lr = precision_score(y_test, yhat_lr, average='micro')
f1_lr = f1_score(y_test, yhat_lr, average='micro')

# Display the confusion matrix for Logistic Regression
cm_lr = confusion_matrix(y_test, yhat_lr)
plt.figure(figsize=(8, 6))
sns.heatmap(cm_lr, annot=True, cmap='Blues')
plt.xlabel('Predicted')
plt.ylabel('True')
plt.title('Confusion Matrix (Logistic Regression)')
plt.show()

# Print the metrics for Logistic Regression
print("Logistic Regression Metrics:")
print("Accuracy Score: ", accuracy_lr)
print("Recall Score: ", recall_lr)
print("Precision Score: ", precision_lr)
print("F1 Score: ", f1_lr)

# Import libraries for SVM
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

# Fit the SVM model
svm_model = SVC(kernel='linear', C=1.0, random_state=42)
svm_model.fit(x_train, y_train)

# Predict using the SVM model
y_pred_svm = svm_model.predict(x_test)

# Calculate and display the metrics for SVM
accuracy_svm = accuracy_score(y_test, y_pred_svm)
recall_svm = recall_score(y_test, y_pred_svm, average='micro')
precision_svm = precision_score(y_test, y_pred_svm, average='micro')
f1_svm = f1_score(y_test, y_pred_svm, average='micro')

# Display the confusion matrix for SVM
cm_svm = confusion_matrix(y_test, y_pred_svm)
plt.figure(figsize=(8, 6))
sns.heatmap(cm_svm, annot=True, cmap='Reds')
plt.xlabel('Predicted')
plt.ylabel('True')
plt.title('Confusion Matrix (SVM)')
plt.show()

# Print the metrics for SVM
print("SVM Metrics:")
print("Accuracy Score: ", accuracy_svm)
print("Recall Score: ", recall_svm)
print("Precision Score: ", precision_svm)
print("F1 Score: ", f1_svm)