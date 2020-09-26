from sklearn.metrics import confusion_matrix

from plot_confusion_matrix import *
from classifiers import *

import csv
import numpy as np
import matplotlib.pyplot as plt

from itertools import permutations

#Try a couple of different multi-label classifiers
#SVM, Random Forest, Gaussian Process Classifiers, ANN

csv_file = 'SQ_feats.csv'
clf_type = 'SVM' #'RF' #'SVM' #'GPC'
cv_type = 'CV' #'LOO' #'CV'
GS = False #Grid Search
use_full_labels = False
handles_combine = False
tool = 'hammer' #'spoon' 'spatula'

cm_plot_show = False

features = []
labels = []

class_labels = {'CONTAIN:contain':0, 'CONTAIN:handle':1, 'CUT:blade':2, 'CUT:handle':3, 
				'FLIP:spatula':4, 'FLIP:handle':5, 'HIT:head':6, 'HIT:handle':7, 'POKE:tip':8, 'POKE:handle':9, 
				'SCOOP:scoop':10, 'SCOOP:handle':11}

class_labels_handles = {'CONTAIN:contain':0, 'CONTAIN:handle':1, 'CUT:blade':2, 'CUT:handle':1, 
				'FLIP:spatula':3, 'FLIP:handle':1, 'HIT:head':4, 'HIT:handle':1, 'POKE:tip':5, 'POKE:handle':1, 
				'SCOOP:scoop':6, 'SCOOP:handle':1}

input_files = {'hammer':'input_hammer.csv', 'spoon':'input_spoon.csv', 'spatula':'input_spatula.csv'}
input_tool_class = {'hammer':[6,7], 'spatula':[4,5], 'spoon':[10,11]}

class_labels_list = [v for v in class_labels.keys()] #ORDER IS CHANGING!!

with open(csv_file) as csvfile:
	reader = csv.reader(csvfile)
	for row in reader:
		row_class = row[0]+':'+row[1]
		if handles_combine:
			labels.append(class_labels_handles[row_class])
		else:
			labels.append(class_labels[row_class])

		row_feats = np.array(row[3:12])
		features.append(row_feats.astype(np.float))

labels = np.array(labels)

X = features
y = labels

scores = 0
#decision function - get confidence for each class on a sample
pred_label = []
true_label = []

if handles_combine:
	classes = range(0,7)
else:
	classes = range(0,12)


clf = classifiers(clf_type, cv_type, GS, X, y)
scores, pred_labels, true_labels = clf.score()

print scores*100
cm = confusion_matrix(true_labels, pred_labels, classes)

if cm_plot_show:
	plt.figure()
	plot_confusion_matrix(cm, classes=classes, title='Confusion matrix')
	plt.show()


test_file = input_files[tool]
pcl_names = []

with open(test_file) as testfile:
	reader = csv.reader(testfile)
	for row in reader:
		row_feats = np.array(row[0:9])
		features.append(row_feats.astype(np.float))
		pcl_names.append(row[9])


tool_class = input_tool_class[tool]
decisions = []
parts_list = range(0,4)

for feats in features:
#	feats.reshape(-1,1)
	decisions.append(clf.decision_function(feats))

part_scores = []

for i in range(4):
	decision = decisions[i]
	decision = decision[0][tool_class[0]:tool_class[1]+1]

	part_scores.append(decision)


#Name the lines in csv with the point clouds so easier to understand the results
#Fix classes for combined handles
#Still need to add attachments and relative part sizes score

permuted_list = permutations(parts_list, 2)
final_dict = {}
final_dict_sorted = {}

for item in permuted_list:
	action_part = item[0]
	grasp_part = item[1]

	total_score = part_scores[action_part][0] + part_scores[grasp_part][1]
	final_dict[pcl_names[action_part]+'+'+pcl_names[grasp_part]] = total_score

#print final_dict

for key, value in sorted(final_dict.iteritems(), key=lambda (k,v): (v,k)):
	print "%s:%s" %(key, value)

print pcl_names