# Try Naive Bayes classifier - Bernoulli and Gaussian
# Try Decision Tree

from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier

from sklearn.model_selection import cross_val_score

import csv
import numpy as np
import ast

csv_exp_data = 'raw_feats_bal.csv'

clf =  'SVM' #'DT' #'NB'
data = []
labels = []
test = []
test_labels = []
num_cv = 3

with open(csv_exp_data) as csvfile:
	reader = csv.reader(csvfile)
	next(reader, None)
	for row in reader:
		feats = [int(row[0]), int(row[1])] + map(float, ast.literal_eval(row[2]))
		data.append(feats)
		labels.append(int(row[3])) #Classify based on effect for the individual binary classifiers case

if clf == 'NB': #Does badly on attributes that were not in the training dataset
	clf = GaussianNB()
	clf.fit(data, labels)
	scores = cross_val_score(clf, data, labels, cv=num_cv)

elif clf == 'DT':
	clf = DecisionTreeClassifier(random_state=0)
	clf.fit(data, labels)
	scores = cross_val_score(clf, data, labels, cv=num_cv)

elif clf == 'SVM':
	clf = SVC(gamma='auto')
	clf.fit(data, labels)
	scores = cross_val_score(clf, data, labels, cv=num_cv)

elif clf == 'RF':
	clf = RandomForestClassifier(n_estimators=10, max_depth=2, random_state=0)
	clf.fit(data, labels)
	scores = cross_val_score(clf, data, labels, cv=num_cv)

print np.mean(scores)
#print clf.predict([2,0,4,0])

#print clf.score(test, test_labels)
#print clf.predict([2,4,4,0])