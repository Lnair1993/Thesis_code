from sklearn.externals import joblib
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle
from sklearn.preprocessing import Normalizer
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
#from plot_confusion_matrix import plot_confusion_matrix

import csv
import ast
import numpy as np
import random
import os
import util
from matplotlib import pyplot as plt

from keras.models import model_from_json
from keras.models import Sequential, Model, load_model
from keras.layers import Dense, Input, Lambda, merge
import keras.backend as K
from keras import optimizers
from keras import regularizers

def sigmoid(z):
    return 1/(1+np.exp(-z))

def features_scio(csv_file):
    # Take csv file and retrieve scio_processed_data corresponding to input
    features = {}
    obj_materials = {}
    wavelengthCount = 331
    with open(csv_file) as f:
        reader = csv.reader(f)
        for idx, row in enumerate(reader):
            if idx == 10:
                wavelengths = [float(r.strip().split('_')[-1].split()[0]) + 740.0 for r in row[10:wavelengthCount+10]]
            try:
                int(row[0]) # To skip first few rows until first integer encountered
                if '.ply' not in row[3]:
                    obj_name = row[3] + '.ply'
                else:
                    obj_name = row[3]
                features_list = [float(elt) for elt in row[10:wavelengthCount+10]]
                features_list = firstDeriv(features_list, wavelengths)
                features[obj_name] = features_list

                material_name = row[4]
                obj_materials[obj_name] = row[4]
            except:
                pass

    return features, obj_materials

def firstDeriv(x, wavelengths):
    # First derivative of measurements with respect to wavelength
    x = [np.copy(x)]
    for i, xx in enumerate(x):
        dx = np.zeros(xx.shape, np.float)
        dx[0:-1] = np.diff(xx)/np.diff(wavelengths)
        dx[-1] = (xx[-1] - xx[-2])/(wavelengths[-1] - wavelengths[-2])
        x[i] = dx
    return x[0]

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

def materials_dualNN(scio_data_processed, trained_embeddings, trained_wts, scaler_file):
    old_tool_encoding_full = np.load(trained_embeddings)
    old_tool_encoding = np.mean(old_tool_encoding_full,axis=0)
    old_tool_encoding = old_tool_encoding.reshape(old_tool_encoding.shape[0],1)
    scio_data_processed = np.array([scio_data_processed])

    scale = 'scaler' #'scaler' #'scaler' or None
    if scale is not None:
        scaler = joblib.load(scaler_file)
        scio_data_processed = scaler.transform(scio_data_processed)
        input_shape = scio_data_processed.shape[1:]
    else:
        input_shape = scio_data_processed.shape[1:]

    #print "Array shape is: \n"
    #print scio_data_processed.shape[1]

     ## create the model
    input = Input(input_shape)
    x = Dense(426,  activation='relu', kernel_regularizer=regularizers.l2(0.001),name='Features1')(input)
    x = Dense(284,  activation='relu', kernel_regularizer=regularizers.l2(0.001),name='Features2')(x)
    x = Dense(128,  activation='relu', kernel_regularizer=regularizers.l2(0.001), name='Features3')(x)

    ## Base Network
    base_network = Model(inputs=input, outputs=x)

    ## Create the inputs
    input_features_1 = Input(input_shape)
    input_features_2 = Input(input_shape)

    ## Tool Encodings
    tool_encoding_1 = base_network(input_features_1)
    tool_encoding_2 = base_network(input_features_2)

    ## Similarity Layer
    l1_distance_layer = Lambda(lambda tensors: K.abs(tensors[0]-tensors[1]), name='L1_Distance')
    l1_distance = l1_distance_layer([tool_encoding_1, tool_encoding_2])

    ## Distance Fusion and Final Prediction Layer
    fusion_layer = Dense(64, activation='relu', kernel_regularizer=regularizers.l2(0.001), name='Fusion')(l1_distance)
    prediction = Dense(1, activation='sigmoid', name='Final_Layer')(fusion_layer)
    model = Model(inputs=[input_features_1, input_features_2], outputs=prediction)

    ## Compile and Fit the model
    model.compile(loss='binary_crossentropy', optimizer=optimizers.Adam(lr=0.000001), metrics=['binary_accuracy'])
    model.load_weights(trained_wts)

    ## Test new data point
    tool_features = scio_data_processed.reshape((1,331))
    new_tool_encoding = base_network.predict(tool_features)

    ## Calculate the L1 distance betweent the test embedding and trained embedding
    l1_distance_new_layer = np.absolute(new_tool_encoding.T-old_tool_encoding)

    ## Load the weights of the required layers
    layer_dict = dict([(layer.name, layer) for layer in model.layers])
    weights_fusion_layer = layer_dict['Fusion'].get_weights()
    weights_final_layer = layer_dict['Final_Layer'].get_weights()
    weights_fusion_layer = np.array(weights_fusion_layer)
    weights_final_layer = np.array(weights_final_layer)

    ## Compute the prediction of last layer using Knn
    z1 = np.dot(l1_distance_new_layer.T,weights_fusion_layer[0]) + weights_fusion_layer[1]
    a1 = np.maximum(z1,0)
    z2 = np.dot(a1,weights_final_layer[0]) + weights_final_layer[1]
    a2 = sigmoid(z2)

    return a2[0][0] #Probability of successful match

# MAIN PROGRAM
# Read from final dataset - read materials
# Compute features for each
# Assign ground truth
# Compute dual NN output
# Print results

scio_dataset = 'test_data.csv'
trained_model = 'materials_NN.json'
trained_wts = 'materials_wts.h5'

obj_features, obj_materials = features_scio(scio_dataset)
tool_types = {'hit':['wood', 'metal'], 'flip':['wood', 'metal', 'plastic'], 'squeegee':['foam'], 'screw':['metal','plastic'], 'scoop':['plastic','wood','metal'], 'rake':['plastic','wood','metal']}
results = {'hit':0, 'flip':0, 'squeegee':0, 'screw':0, 'scoop':0, 'rake':0}

trained_embeddings_folder = '/home/lnair3/Nimbus_ws/src/nimbus_explore/src/Dual_NN_files/Embeddings/'
trained_wts_folder = '/home/lnair3/Nimbus_ws/src/nimbus_explore/src/Dual_NN_files/Model/'
trained_scaler_folder = '/home/lnair3/Nimbus_ws/src/nimbus_explore/src/Dual_NN_files/Scalar_wts/'

material_values = ['plastic', 'wood', 'metal', 'foam', 'paper']

for obj in obj_materials.keys():
    print obj
    for tool_type in tool_types.keys():
        #trained_embeddings = 'embeddings_material_prop_' + tool_type + '.npy'
        #trained_wts = 'material_prop_weights_' + tool_type + '.h5'
        #scaler_file = 'scaler_materials_' + tool_type + '.save'

        #prediction = materials_dualNN(obj_features[obj], trained_embeddings_folder + trained_embeddings, trained_wts_folder + trained_wts, trained_scaler_folder + scaler_file)
        #if prediction > 0.5 and obj_materials[obj] in tool_types[tool_type]:
        #    results[tool_type] += 1
        prediction = materials_predict(obj_features[obj], trained_model, trained_wts)
        if material_values[prediction[0]] == obj_materials[obj] and material_values[prediction[0]] in tool_types[tool_type]:
            results[tool_type] += 1

print results



