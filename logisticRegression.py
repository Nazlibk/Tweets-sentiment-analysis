""" This file is the implementation of Logistic Regression. After fitting the regressor, this file uses pickle library
for serializing he training data. So, by reloading this trained data, it can be used for predicting in the future.
"""
import pandas as pd
import re
import pickle

# Importing the dataset
dataset = pd.read_csv('labeledTweets3Classes.csv')
X = dataset.iloc[:, :-1].values
y = dataset.iloc[:, -1].values

# Preprocessing (remove urls, @s and numbers from texts)
from nltk.stem.porter import PorterStemmer
porter_stemmer = PorterStemmer()
for i in range(len(X)):
    X[i, 1] = re.sub(r"http\S+|\d+|@[A-Za-z0-9]+", "", str(X[i, 1]))
    X[i, 1] = ''.join(porter_stemmer.stem(str(X[i, 1])))

# Splitting the dataset to Training set and Test set
from sklearn.model_selection import train_test_split, cross_val_score, cross_val_predict
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 1/3,  random_state = 0)

# TF-IDF
from sklearn.feature_extraction.text import TfidfVectorizer
tfidf_vect = TfidfVectorizer(max_features=10000, ngram_range=(1, 1), stop_words="english", use_idf=True, smooth_idf=True, min_df=4)
X_train_tfidf =  tfidf_vect.fit_transform(X_train[:, 1])
X_test_tfidf =  tfidf_vect.fit_transform(X_test[:, 1])

# Logistic Regression
# I tuned the model with parameters below which are given the best results. You can change the parameters if it is needed.
from sklearn.linear_model import LogisticRegression
regressor = LogisticRegression(solver='sag', C=20, max_iter=1000)
regressor.fit(X_train_tfidf, y_train)

# Serializing our model to a file called regressorModel.pkl
pickle.dump(regressor, open("regressorModel.pkl","wb"))

# 10-Fold cross validation
scores = cross_val_score(regressor, X_train_tfidf, y_train, cv=10)

print("\nCross validation accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
from sklearn import metrics
predicted = cross_val_predict(regressor, X_test_tfidf, y_test, cv=10)
print("Prediction accuracy: %0.2f" % metrics.accuracy_score(y_test, predicted))
print("Confusion matrix:\n%s" % metrics.confusion_matrix(y_test, predicted))