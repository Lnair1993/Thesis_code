import os, sys
import numpy as np
import cPickle as pickle
import csv

from keras.models import Sequential, Model
from keras.layers import Dense, Input, Lambda, Dropout, merge
import keras.backend as K
from keras import optimizers
from keras import regularizers
from keras.utils import plot_model
from keras.utils.np_utils import to_categorical

from sklearn.preprocessing import Normalizer, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.utils import shuffle
from sklearn.externals import joblib

import util
import random

np.random.seed(11)

def sigmoid(z):
    return 1/(1+np.exp(-z))

if __name__=="__main__":
    materials = ['plastic', 'fabric', 'paper', 'wood', 'metal', 'foam']

    plastics = ['HDPE', 'PET', 'polyethyleneBlue', 'polyethyleneGreen', 'polyethyleneRed', 'polyethyleneYellow', 'PP', 'PVC', 'thermoPolypropylene', 'thermoTeflon']
    fabrics = ['cottonCanvas', 'cottonSweater', 'cottonTowel', 'denim', 'felt', 'flannel', 'gauze', 'linen', 'satin', 'wool']
    papers = ['cardboard', 'constructionPaperGreen', 'constructionPaperOrange', 'constructionPaperRed', 'magazinePaper', 'newspaper', 'notebookPaper', 'printerPaper', 'receiptPaper', 'textbookPaper']
    woods = ['ash', 'cherry', 'curlyMaple', 'hardMaple', 'hickory', 'redCedar', 'redElm', 'redOak', 'walnut', 'whiteOak']
    metals = ['aluminum', 'aluminumFoil', 'brass', 'copper', 'iron', 'lead', 'magnesium', 'steel', 'titanium', 'zinc']
    objects = [plastics, fabrics, papers, woods, metals]

    foam = ['styrofoam_cup', 'ball', 'pie', 'dinosaur_yellow', 'dinosaur_blue', 'dinosaur_purple', 'dinosaur_green', 'dinosaur_orange', 'toad_mario', 'baseball', 'white_sheets', 'black_sheets', 'styrofoam_block', 'sandal']
    objects2 = [[], [], [], [], [], foam]

    saveFilename = os.path.join('data', 'smm50_scio.pkl')
    with open(saveFilename, 'rb') as f:
        X, y_materials, y_objects, wavelengths = pickle.load(f)

    not_fabrics_indices = [i for i,x in enumerate(y_objects) if x not in fabrics]
    X_new_no_fabric = [x for i,x in enumerate(X) if i in not_fabrics_indices]
    y_objects_new_no_fabric = [x for i,x in enumerate(y_objects) if i in not_fabrics_indices]
    y_materials_new_no_fabric = [x for i,x in enumerate(y_materials) if i in not_fabrics_indices]
    X = X_new_no_fabric
    y_materials = y_materials_new_no_fabric
    y_objects = y_objects_new_no_fabric




    X2, y_materials2, y_objects2, _ = util.loadScioDataset(pklFile='scio_everyday_objects_expanded', csvFile='scio_everyday_objects_expanded', materialNames=materials, objectNames=objects2)
    # print np.shape(X), np.shape(y_materials), np.shape(y_objects), np.shape(X2), np.shape(y_materials2), np.shape(y_objects2)


    X = np.concatenate([X, X2], axis=0)
    y_materials = np.concatenate([y_materials, y_materials2], axis=0)
    y_objects = np.concatenate([y_objects, y_objects2], axis=0)
    wavelengths = np.array(wavelengths)
    # print np.shape(X), np.shape(y_materials), np.shape(y_objects), np.shape(X2), np.shape(y_materials2), np.shape(y_objects2)

    ## Create a Set of unseen data
    Unseen_Plastic = ['PET', 'PP']
    Unseen_Wood = ['redOak', 'walnut']
    Unseen_Metal = ['iron', 'steel']
    Unseen_Foam = ['ball', 'pie']
    Unseen_Paper = ['newspaper', 'notebookPaper']

    Unseen_Stuff = np.concatenate([Unseen_Plastic, Unseen_Wood, Unseen_Metal, Unseen_Foam, Unseen_Paper], axis=0)
    unseen_indices = [i for i,x in enumerate(y_objects) if x in Unseen_Stuff]
    unseen_indices = np.array(unseen_indices)
    print(unseen_indices.shape)
    seen_indices = [i for i,x in enumerate(y_objects) if x not in Unseen_Stuff]
    seen_indices = np.array(seen_indices)
    print(seen_indices.shape)

    X_unseen = [x for i,x in enumerate(X) if i in unseen_indices]
    X_unseen = np.array(X_unseen)
    print(X_unseen.shape)
    y_materials_unseen = [x for i,x in enumerate(y_materials) if i in unseen_indices]
    y_materials_unseen = np.array(y_materials_unseen)
    print(y_materials_unseen.shape)
    y_objects_unseen = [x for i,x in enumerate(y_objects) if i in unseen_indices]
    y_objects_unseen = np.array(y_objects_unseen)
    print(y_objects_unseen.shape)

    X_seen = [x for i,x in enumerate(X) if i not in unseen_indices]
    X_seen = np.array(X_seen)
    print(X_seen.shape)
    y_materials_seen = [x for i,x in enumerate(y_materials) if i not in unseen_indices]
    y_materials_seen = np.array(y_materials_seen)
    print(y_materials_seen.shape)
    y_objects_seen = [x for i,x in enumerate(y_objects) if i not in unseen_indices]
    y_objects_seen = np.array(y_objects_seen)
    print(y_objects_seen.shape)
    #
    test_array_indices = np.random.choice(unseen_indices,10)
    for x, ym, yo in zip(X_unseen, y_materials_unseen, y_objects_unseen):
        with open("/home/nithin/Desktop/ThreeDCV/Research/Material_Prop_Test.csv", "a") as output:
            output.write("\n")
            output.write(yo)
            output.write(",")
            output.write(str(ym))
            output.write(",")
            writer = csv.writer(output, lineterminator='\n')
            writer.writerows([x])
    #
    # samples = 1
    # X_new_test = []
    # y_materials_new_test = []
    # y_objects_new_test = []
    # for x, ym, yo in zip(X_unseen, y_materials_unseen, y_objects_unseen):
    #     # print yo, len(y_objects_new[y_objects_new == yo]), len(y_objects)
    #     if yo not in y_objects_new_test or len(np.array(y_objects_new_test)[np.array(y_objects_new_test) == yo]) < samples:
    #         X_new_test.append(x)
    #         y_materials_new_test.append(ym)
    #         y_objects_new_test.append(yo)
    #
    # X = X_new
    # y_materials = y_materials_new
    # y_objects = y_objects_new
