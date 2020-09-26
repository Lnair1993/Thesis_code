from sklearn.model_selection import LeaveOneOut
from sklearn.model_selection import train_test_split
from scipy.stats import randint as sp_randint

import numpy as np

def CV_init(CV_type, data, labels, num_cv):
	if CV_type == 'LOO':
		CV = LeaveOneOut()
		return CV.split(data)
	elif CV_type == 'CV':
		X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=1/num_cv, random_state=0)
		return [X_train, X_test, y_train, y_test]
	else:
		return data

def random_grid_gen(clf_type):

	if clf_type == 'RF':
		param_dist = {"n_estimators": [10, 20, 30, 40, 50],
				"max_depth": [3, None],
            	"bootstrap": [True, False],
            	"criterion": ["gini", "entropy"]}
	elif clf_type == 'SVM':
		param_dist = {"multi_class": ["ovr", "crammer_singer"]}

	return param_dist

