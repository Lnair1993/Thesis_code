# Try Naive Bayes classifier - Bernoulli and Gaussian
# Try Decision Tree

from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier

from sklearn.model_selection import cross_val_score

import csv
import numpy as np


#[0, 0, 0, 0]

#csv_exp_data = 'csv_balanced.csv'
csv_exp_data = 'csv_balanced_pierce_grasp_no_effect.csv'
#csv_file = 'stabby_test.csv'
#csv_exp_data = 'stabby_data.csv'
clf =  'SVM' #'DT' #'NB'
data = []
labels = []
test = []
test_labels = []
num_cv = 3

bin_clf = False

with open(csv_exp_data) as csvfile:
	reader = csv.reader(csvfile)
	next(reader, None)
	for row in reader:
		if bin_clf:
			feats = [row[1]] + row[3:6]
		else:
			feats = [row[0]] + row[2:5] #No effects column
		feats = map(int, feats)
		data.append(feats)
		labels.append(int(row[1])) #Classify based on effect for the individual binary classifiers case

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


'''with open(csv_file) as csv_test:
	reader = csv.reader(csv_test)
	next(reader, None)
	for row in reader:
		test_feats = [row[1]] + row[3:6]
		test_feats = map(int, test_feats)
		test.append(test_feats)
		test_labels.append(int(row[0]))'''

print np.mean(scores)
#print clf.predict([2,0,4,0])

#print clf.score(test, test_labels)
print clf.predict([2,4,4,0])