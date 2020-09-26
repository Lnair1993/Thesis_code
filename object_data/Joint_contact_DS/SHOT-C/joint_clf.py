from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier

from sklearn.model_selection import cross_val_score

import csv
import numpy as np
import ast

csv_exp_data = 'temp_4.csv'

clf =  'RF' #'DT' #'NB'
data = []
labels = []
test = []
test_labels = []
num_cv = 3

joint_num = {'revolute':1, 'fixed':0}
contact_num = {'point':1, 'no':0}

with open(csv_exp_data) as csvfile:
	reader = csv.reader(csvfile)
	next(reader, None) # Skip first row
	for row in reader:
		feats = map(float, row[3:len(row)])
		data.append(feats)
		labels.append(contact_num[row[2].strip()]) #Classify based on effect for the individual binary classifiers case

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