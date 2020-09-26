import os, sys
import numpy as np
import cPickle as pickle

import numpy as np
import tensorflow as tf
import random as rn
np.random.seed(0)
rn.seed(0)
session_conf = tf.ConfigProto(intra_op_parallelism_threads=1, inter_op_parallelism_threads=1)
from keras import backend as K
tf.set_random_seed(0)
sess = tf.Session(graph=tf.get_default_graph(), config=session_conf)
K.set_session(sess)

from keras.models import Sequential, Model
from keras.layers import Dense, Dropout, LeakyReLU
from keras.optimizers import Adam
from keras.utils.np_utils import to_categorical

from sklearn.preprocessing import Normalizer, StandardScaler
from sklearn.svm import SVC
from sklearn.model_selection import StratifiedKFold

import util
from matplotlib import pyplot as plt
from plot_confusion_matrix import plot_confusion_matrix
from sklearn.metrics import confusion_matrix


#scale = None #'scaler' #None
classifier = 'nn'
predictPiercability = True #True #False

if predictPiercability:
    scale = 'scaler'
else:
    scale = None

materials = ['plastic', 'wood', 'metal', 'foam']

plastics = ['HDPE', 'PET', 'polyethyleneBlue', 'polyethyleneGreen', 'polyethyleneRed', 'polyethyleneYellow', 'PP', 'PVC', 'thermoPolypropylene', 'thermoTeflon']
woods = ['ash', 'cherry', 'curlyMaple', 'hardMaple', 'hickory', 'redCedar', 'redElm', 'redOak', 'walnut', 'whiteOak']
metals = ['aluminum', 'aluminumFoil', 'brass', 'copper', 'iron', 'lead', 'magnesium', 'steel', 'titanium', 'zinc']
objects = [plastics, woods, metals]

foam = ['styrofoam_cup', 'ball', 'pie', 'dinosaur_yellow', 'dinosaur_blue', 'dinosaur_purple', 'dinosaur_green', 'dinosaur_orange', 'toad_mario', 'baseball', 'white_sheets', 'black_sheets', 'styrofoam_block', 'sandal']
objects2 = [[], [], [], foam]

saveFilename = os.path.join('data', 'smm50_scio.pkl')
with open(saveFilename, 'rb') as f:
    X, y_materials, y_objects, wavelengths = pickle.load(f)
    # Keep only training data for the materials/objects specified above
    flatmats = np.array(objects).flatten()
    X_new = []
    y_materials_new = []
    y_objects_new = []
    for x, ym, yo in zip(X, y_materials, y_objects):
        if yo in flatmats:
            X_new.append(x)
            y_materials_new.append(ym)
            y_objects_new.append(yo)
    X = X_new
    y_materials = y_materials_new
    y_objects = y_objects_new
    # Fix labels
    y_materials = np.array(y_materials)
    y_materials[y_materials == 3] = 1
    y_materials[y_materials == 4] = 2
print set(y_materials)

X2, y_materials2, y_objects2, _ = util.loadScioDataset(pklFile='scio_everyday_objects_expanded_test', csvFile='scio_everyday_objects_expanded', materialNames=materials, objectNames=objects2)
print np.shape(X), np.shape(y_materials), np.shape(y_objects), np.shape(X2), np.shape(y_materials2), np.shape(y_objects2)
print set(y_materials2)

X = np.concatenate([X, X2], axis=0)
y_materials = np.concatenate([y_materials, y_materials2], axis=0)
y_objects = np.concatenate([y_objects, y_objects2], axis=0)
wavelengths = np.array(wavelengths)
print 'Data dimensions of combined training dataset:', np.shape(X), np.shape(y_materials), np.shape(y_objects), np.shape(X2), np.shape(y_materials2), np.shape(y_objects2)
print set(y_materials)

X_test, y_materials_test, y_objects_test, _ = util.loadScioDataset(pklFile='test_data', csvFile='test_data', materialNames=materials, objectNames=None)
print 'Data dimenstions of test data:', np.shape(X_test), np.shape(y_materials_test), np.shape(y_objects_test)
print set(y_materials_test)

# Use only 10 samples from each object
samples = 10
X_new = []
y_materials_new = []
y_objects_new = []
for x, ym, yo in zip(X, y_materials, y_objects):
    # print yo, len(y_objects_new[y_objects_new == yo]), len(y_objects)
    if yo not in y_objects_new or len(np.array(y_objects_new)[np.array(y_objects_new) == yo]) < samples:
        X_new.append(x)
        y_materials_new.append(ym)
        y_objects_new.append(yo)
X = X_new
y_materials = y_materials_new
y_objects = y_objects_new
print 'Data dimensions for 10 samples per object', np.shape(X), np.shape(y_materials), np.shape(y_objects)

X_train = util.firstDeriv(X, wavelengths)
y_train = np.array(y_materials)
X_test = util.firstDeriv(X_test, wavelengths)
y_test = np.array(y_materials_test)

if predictPiercability:
    # Switch from predicting materials to predicting piercability of an object (binary output)
    y_new = []
    for ym, yo in zip(y_materials, y_objects):
        # y_new.append(1 if materials[ym] == 'foam' and yo not in ['toad_mario', 'baseball', 'sandal'] else 0)
        y_new.append(1 if materials[ym] == 'foam' else 0)
    y_train = np.array(y_new)

    y_new_ = []
    for ym, yo in zip(y_materials_test, y_objects_test):
        y_new_.append(1 if materials[ym] == 'foam' else 0)
    y_test = np.array(y_new_)

accuracies = []

if scale is not None:
    scaler = StandardScaler() if scale == 'scale' else Normalizer()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)
    # print np.min(X_train), np.max(X_train)
    # print np.min(X_test), np.max(X_test)

if classifier == 'svm':
    model = SVC(C=1, kernel='rbf')
    model.fit(X_train, y_train)
    print 'Accuracy:', model.score(X_test, y_test)
elif classifier == 'nn':
    #num_classes = len(set(y_materials))
    num_classes = len(set(y_train))
    print set(y_materials), num_classes
    y_train = to_categorical(y_train, num_classes)
    y_test = to_categorical(y_test, num_classes)

    model = Sequential()
    model.add(Dense(128, activation='relu', input_shape=(np.shape(X_train)[-1],)))
    #model.add(Dropout(0.15))
    model.add(Dense(128, activation='relu'))
    #model.add(Dropout(0.15))
    model.add(Dense(num_classes, activation='softmax'))

    # d = [64]*2 + [32]*2
    # model = Sequential()
    # model.add(Dense(d[0], activation='linear', input_dim=np.shape(X)[-1]))
    # # model.add(Dropout(0.05))
    # model.add(Dropout(0.25))
    # model.add(LeakyReLU())
    # for dd in d[1:]:
    #     model.add(Dense(dd, activation='linear'))
    #     # model.add(Dropout(0.05))
    #     model.add(Dropout(0.25))
    #     model.add(LeakyReLU())
    # model.add(Dense(materialCount, activation='softmax'))
    # model.compile(loss='categorical_crossentropy', optimizer=Adam(lr=0.0005), metrics=['accuracy'])

    # Adam(lr=0.0001)
    model.compile(loss='categorical_crossentropy' if not predictPiercability else 'binary_crossentropy', optimizer='adam', metrics=['accuracy'])

    model.fit(X_train, y_train, batch_size=16, epochs=40, verbose=1) #, validation_data=(X_test, y_test))
    model_json = model.to_json()

    if predictPiercability:
        with open('pierce_NN.json', 'w') as json_file:
            json_file.write(model_json)
            model.save_weights('pierce_wts.h5')
    else:
        with open('materials_NN.json', 'w') as json_file:
            json_file.write(model_json)
            model.save_weights('materials_wts.h5')

    loss, accuracy = model.evaluate(X_test, y_test, verbose=1)
    predicted_labels = model.predict_classes(X_test, batch_size=16)
    print 'Accuracy:', accuracy

print y_test

if predictPiercability:
    cm = confusion_matrix(np.argmax(y_test, 1), predicted_labels, labels=range(2))
    print np.array2string(cm.astype('float') / cm.sum(axis=1)[:, np.newaxis], separator=', ')
    plt.figure()
    plot_confusion_matrix(cm, classes=['non-pierceable','pierceable'], normalize=True, title='Confusion matrix')
else:
    cm = confusion_matrix(np.argmax(y_test, 1), predicted_labels, labels=range(len(materials)))
    print np.array2string(cm.astype('float') / cm.sum(axis=1)[:, np.newaxis], separator=', ')
    plt.figure()
    plot_confusion_matrix(cm, classes=materials, normalize=True, title='Confusion matrix')

plt.show()