from sklearn.externals import joblib

#from plot_confusion_matrix import plot_confusion_matrix

import csv
import ast
import numpy as np
from matplotlib import pyplot as plt

from keras.models import model_from_json
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score

from sklearn.preprocessing import Normalizer

# Write different functions for:

# ---------- Section 1 ----------
# Define a function for processing the retrieved data
# Define a function for retrieving sensor data from web
# Define a function for creating features out of it - CHECK
# Define a function for predicting pierceability using specified model - CHECK

# Change attributes of the MG_object instance

def pierce_predict(scio_data_processed, trained_model, trained_wts):
    json_file = open(trained_model, 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)

    # load weights into new model
    loaded_model.load_weights(trained_wts)
    loaded_model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])

    # Normalize the data
    scaler = Normalizer()
    obj = scaler.transform([scio_data_processed])
    pierce_value = loaded_model.predict_classes(np.array(obj))

    return pierce_value # Potentially return the prediction score or probability as well?

def materials_predict(scio_data_processed, trained_model, trained_wts):
    json_file = open(trained_model, 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    # load weights into new model
    loaded_model.load_weights(trained_wts)
    loaded_model.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
    material_class = loaded_model.predict_classes(np.array([scio_data_processed]))

    return material_class 

def features_scio(csv_file):
    # Take csv file and retrieve scio_processed_data corresponding to input
    features = {}
    wavelengthCount = 331
    with open(csv_file) as f:
        reader = csv.reader(f)
        for idx, row in enumerate(reader):
            if idx == 10:
                wavelengths = [float(r.strip().split('_')[-1].split()[0]) + 740.0 for r in row[10:wavelengthCount+10]]
            try:
                int(row[0]) # To skip first few rows until first integer encountered
                obj_name = row[4]
                features_list = [float(elt) for elt in row[10:wavelengthCount+10]]
                features_list = firstDeriv(features_list, wavelengths)
                features[obj_name] = features_list
            except:
                pass

    return features

def firstDeriv(x, wavelengths):
    # First derivative of measurements with respect to wavelength
    x = [np.copy(x)]
    for i, xx in enumerate(x):
        dx = np.zeros(xx.shape, np.float)
        dx[0:-1] = np.diff(xx)/np.diff(wavelengths)
        dx[-1] = (xx[-1] - xx[-2])/(wavelengths[-1] - wavelengths[-2])
        x[i] = dx
    return x[0]