from sklearn.svm import LinearSVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF

from sklearn.model_selection import RandomizedSearchCV
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import cross_val_predict
from sklearn.model_selection import cross_val_score

from CV_init import *
import numpy as np

class classifiers:
	def __init__(self, clf_type, CV_type, GS, data, labels, num_CV = 3):
		self.num_cv = num_CV
		self.clf_type = clf_type
		self.X = data
		self.y = labels
		self.cv_type = CV_type
		self.GS = GS

		self.clf = self.clf_init(clf_type, GS) # Function to initialize the classifier
		self.data_split = CV_init(CV_type, data, labels, num_CV)

	def clf_init(self, clf_type, GS):
		if clf_type == 'SVM':
			clf = LinearSVC(multi_class='crammer_singer', random_state=0)
		elif clf_type == 'RF':
			clf = RandomForestClassifier(max_depth=2, random_state=0)
		elif clf_type == 'GPC':
			clf = GaussianProcessClassifier(1.0 * RBF(1.0))

		if GS:
			random_grid = random_grid_gen(clf_type)
			clf = GridSearchCV(estimator=clf, param_grid=random_grid, cv=self.num_cv)
		return clf


	def score(self):
		scores = []
		pred_labels = []
		true_labels = []

		if self.cv_type == 'LOO':
			for train_index, test_index in self.data_split:
				train_index = train_index.tolist()
				test_index = test_index.tolist()

				train_data = [(self.X[i], self.y[i]) for i in train_index]
				test_data = [(self.X[i], self.y[i]) for i in test_index]

				X_train, y_train = map(list, zip(*train_data))
				X_test, y_test = map(list, zip(*test_data))

				self.clf.fit(X_train, y_train)
				scores.append(self.clf.score(X_test, y_test))

				pred_labels.append(self.clf.predict(X_test))
				true_labels.append(y_test)

			return np.mean(scores), pred_labels, true_labels

		elif self.cv_type == 'CV':
			scores = cross_val_score(self.clf, self.X, self.y, cv=self.num_cv)
			pred_labels = cross_val_predict(self.clf, self.X, self.y, cv=self.num_cv)
			true_labels = self.y

			if not self.GS:
				self.clf.fit(self.data_split[0], self.data_split[2])

			return np.mean(scores), pred_labels, true_labels

	def predict(self, query):
		return self.clf.predict(query)

	def decision_function(self, query):
		return self.clf.decision_function(query)

