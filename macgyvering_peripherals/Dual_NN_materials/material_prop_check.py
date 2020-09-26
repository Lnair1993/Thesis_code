'''import os, sys
import numpy as np
import cPickle as pickle

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


# object_class = 'cut'
# object_class = 'flip'
object_class = 'hit'
# object_class = 'scoop'
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

# Use only 10 samples from each object
samples = 10
X_new = []
y_materials_new = []
y_objects_new = []
for x, ym, yo in zip(X_seen, y_materials_seen, y_objects_seen):
    # print yo, len(y_objects_new[y_objects_new == yo]), len(y_objects)
    if yo not in y_objects_new or len(np.array(y_objects_new)[np.array(y_objects_new) == yo]) < samples:
        X_new.append(x)
        y_materials_new.append(ym)
        y_objects_new.append(yo)

X_new_test = []
y_materials_new_test = []
y_objects_new_test = []
for x, ym, yo in zip(X_unseen, y_materials_unseen, y_objects_unseen):
    # print yo, len(y_objects_new[y_objects_new == yo]), len(y_objects)
    if yo not in y_objects_new_test or len(np.array(y_objects_new_test)[np.array(y_objects_new_test) == yo]) < samples:
        X_new_test.append(x)
        y_materials_new_test.append(ym)
        y_objects_new_test.append(yo)

X = X_new
y_materials = y_materials_new
y_objects = y_objects_new

X = util.firstDeriv(X, wavelengths)
Y = np.array(y_materials)

X_test = util.firstDeriv(X_new_test, wavelengths)
Y_test = np.array(y_materials_new_test)

Y[Y==0]=6 ## Plastic
Y[Y==2]=7 ## Paper
Y[Y==3]=8 ## Wood
Y[Y==4]=9 ## Metal
Y[Y==5]=10 ## Foam
print(Y)

Y_test[Y_test==0]=6 ## Plastic
Y_test[Y_test==2]=7 ## Paper
Y_test[Y_test==3]=8 ## Wood
Y_test[Y_test==4]=9 ## Metal
Y_test[Y_test==5]=10 ## Foam
print(Y_test)

if object_class == 'cut':
    Y[Y==6] = 1
    Y[Y==7] = 0
    Y[Y==8] = 1
    Y[Y==9] = 1
    Y[Y==10] = 0
    print(Y)
    print("cut")
    Y_test[Y_test==6] = 1
    Y_test[Y_test==7] = 0
    Y_test[Y_test==8] = 1
    Y_test[Y_test==9] = 1
    Y_test[Y_test==10] = 0
    print(Y_test)
    print("cut")
elif object_class =='flip':
    Y_test[Y_test==6] = 0
    Y_test[Y_test==7] = 0
    Y_test[Y_test==8] = 1
    Y_test[Y_test==9] = 1
    Y_test[Y_test==10] = 0
    print(Y_test)
    print("flip")
    Y[Y==6] = 0
    Y[Y==7] = 0
    Y[Y==8] = 1
    Y[Y==9] = 1
    Y[Y==10] = 0
    print(Y)
    print("flip")
elif object_class == 'hit':
    Y_test[Y_test==6] = 0
    Y_test[Y_test==7] = 0
    Y_test[Y_test==8] = 1
    Y_test[Y_test==9] = 1
    Y_test[Y_test==10] = 0
    print(Y_test)
    print("hit")
    Y[Y==6] = 0
    Y[Y==7] = 0
    Y[Y==8] = 1
    Y[Y==9] = 1
    Y[Y==10] = 0
    print(Y)
    print("hit")
elif object_class == 'scoop':
    Y_test[Y_test==6] = 1
    Y_test[Y_test==7] = 0
    Y_test[Y_test==8] = 1
    Y_test[Y_test==9] = 1
    Y_test[Y_test==10] = 0
    print(Y)
    print("scoop")
    Y[Y==6] = 1
    Y[Y==7] = 0
    Y[Y==8] = 1
    Y[Y==9] = 1
    Y[Y==10] = 0
    print(Y)
    print("scoop")

# X,Y = shuffle(X,Y,random_state=1)
# X_train, X_test, Y_train, Y_test = train_test_split(X,Y,test_size=0.1,random_state=1)

## Preprocessing
scaler_filename = "/home/nithin/Desktop/ThreeDCV/Research/Material_Prop/scaler_materials_hit.save"
scaler = joblib.load(scaler_filename)
X_test = scaler.transform(X_test)
input_shape = X_test.shape[1:]

## Build Model
input = Input(input_shape)
x = Dense(426,  activation='relu', kernel_regularizer=regularizers.l2(0.001),name='Features1')(input)
x = Dropout(0.5)(x)
x = Dense(284,  activation='relu', kernel_regularizer=regularizers.l2(0.001),name='Features2')(x)
x = Dropout(0.5)(x)
x = Dense(128,  activation='relu', kernel_regularizer=regularizers.l2(0.001), name='Features3')(x)
x = Dropout(0.5)(x)

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
# l1_distance_layer = Lambda(lambda tensors: K.square(tensors[0]-tensors[1]), name='L2_Distance')
l1_distance = l1_distance_layer([tool_encoding_1, tool_encoding_2])

## Distance Fusion and Final Prediction Layer
fusion_layer = Dense(64, activation='relu', kernel_regularizer=regularizers.l2(0.001), name='Fusion')(l1_distance)
prediction = Dense(1, activation='sigmoid', name='Final_Layer')(fusion_layer)
model = Model(inputs=[input_features_1, input_features_2], outputs=prediction)

## Compile and Fit the model
model.compile(loss='binary_crossentropy', optimizer=optimizers.Adam(lr=0.001), metrics=['binary_accuracy'])
model.load_weights("/home/nithin/Desktop/ThreeDCV/Research/Material_Prop/material_prop_weights_hit.h5")

## Create Embeddings
old_tool_encoding_full = np.load("/home/nithin/Desktop/ThreeDCV/Research/Material_Prop/embeddings_material_prop_hit.npy")
print(old_tool_encoding_full.shape)
old_tool_encoding = np.mean(old_tool_encoding_full,axis=0)
old_tool_encoding = old_tool_encoding.reshape(old_tool_encoding.shape[0],1)
print(old_tool_encoding.shape)

## Load the weights of the required layers
layer_dict = dict([(layer.name, layer) for layer in model.layers])
weights_fusion_layer = layer_dict['Fusion'].get_weights()
weights_final_layer = layer_dict['Final_Layer'].get_weights()
weights_fusion_layer = np.array(weights_fusion_layer)
weights_final_layer = np.array(weights_final_layer)

## Predictions
y_pred = []
print(Y_test)
for x in X_test:
    tool_features = x.reshape((1,331))
    new_tool_encoding = base_network.predict(tool_features)
    l1_distance_new_layer = np.absolute(new_tool_encoding.T-old_tool_encoding)
    z1 = np.dot(l1_distance_new_layer.T,weights_fusion_layer[0]) + weights_fusion_layer[1]
    a1 = np.maximum(z1,0)
    z2 = np.dot(a1,weights_final_layer[0]) + weights_final_layer[1]
    a2 = sigmoid(z2)
    print(a2)'''

from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.utils import shuffle
from sklearn.externals import joblib
from keras.models import Sequential, Model, load_model
from keras.layers import Dense, Input, Lambda, merge
import keras.backend as K
from keras import optimizers
from keras import regularizers
from keras.utils import plot_model
import numpy as np
import pandas
import random
import os
import csv
import util

def sigmoid(z):
    return 1/(1+np.exp(-z))

if __name__=="__main__":

    folder_path_test_set = "/home/nithin/Desktop/ThreeDCV/Research/Test_Cases/HIT/Material_Descriptor_Cases/"
    folder_path_weights = "/home/nithin/Desktop/ThreeDCV/Research/Material_Prop/HIT_L2/material_prop_weights_hit.h5"
    folder_path_embedding = "/home/nithin/Desktop/ThreeDCV/Research/Material_Prop/HIT_L2/embeddings_material_prop_hit.npy"
    scaler_filename = "/home/nithin/Desktop/ThreeDCV/Research/Material_Prop/HIT_L2/scaler_materials_hit.save"
    wavelengths_filename = "/home/nithin/Desktop/ThreeDCV/Research/Material_Prop/wavelengths.npy"
    wavelengths = np.load(wavelengths_filename)

    ## Load the tool encodings
    old_tool_encoding_full = np.load(folder_path_embedding)
    print(old_tool_encoding_full.shape)
    old_tool_encoding = np.mean(old_tool_encoding_full,axis=0)
    old_tool_encoding = old_tool_encoding.reshape(old_tool_encoding.shape[0],1)
    print(old_tool_encoding.shape)
    #
    for filename in os.listdir(folder_path_test_set):
        print(filename)
        ## Load the data
        data = pandas.read_csv(os.path.join(folder_path_test_set,filename))
        print(data.head())
        X = data.drop(['Object','Material','Label'],axis=1)
        material = data['Material']
        X = util.firstDeriv(X, wavelengths)
        Candidate_Substitutes = data['Object']

        ## Preprocessing the data
        scaler = joblib.load(scaler_filename)
        X = scaler.transform(X)
        input_shape = X.shape[1:]


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
        # l1_distance_layer = Lambda(lambda tensors: K.square(tensors[0]-tensors[1]), name='L1_Distance')
        l1_distance = l1_distance_layer([tool_encoding_1, tool_encoding_2])

        ## Distance Fusion and Final Prediction Layer
        fusion_layer = Dense(64, activation='relu', kernel_regularizer=regularizers.l2(0.001), name='Fusion')(l1_distance)
        prediction = Dense(1, activation='sigmoid', name='Final_Layer')(fusion_layer)
        model = Model(inputs=[input_features_1, input_features_2], outputs=prediction)

        ## Compile and Fit the model
        model.compile(loss='binary_crossentropy', optimizer=optimizers.Adam(lr=0.000001), metrics=['binary_accuracy'])

        ## Load the weights of the network
        model.load_weights(folder_path_weights)
        probabilities = []
        probabilities_1 = []
        probabilities_2 = []
        Rank = [[0 for m in range(X.shape[0])]]

        # Iterate and calculate the probability of each tool being a good substitute
        for i in range(X.shape[0]):
            ## Get the embedding for the test data point
            tool_features = X[i].reshape((1,331))
            new_tool_encoding = base_network.predict(tool_features)

            ## Calculate the L1 distance betweent the test embedding and trained embedding
            l1_distance_new_layer = np.absolute(new_tool_encoding.T-old_tool_encoding)
            # l1_distance_new_layer = np.concatenate((new_tool_encoding.T, old_tool_encoding),axis=0)
            print(l1_distance_new_layer.shape)

            ## Load the weights of the required layers
            layer_dict = dict([(layer.name, layer) for layer in model.layers])
            weights_fusion_layer = layer_dict['Fusion'].get_weights()
            weights_final_layer = layer_dict['Final_Layer'].get_weights()
            weights_fusion_layer = np.array(weights_fusion_layer)
            weights_final_layer = np.array(weights_final_layer)

            # Compute the prediction of last layer using Knn
            z1 = np.dot(l1_distance_new_layer.T,weights_fusion_layer[0]) + weights_fusion_layer[1]
            a1 = np.maximum(z1,0)
            z2 = np.dot(a1,weights_final_layer[0]) + weights_final_layer[1]
            a2 = sigmoid(z2)
            # new_element = {Candidate_Substitutes[i]:a2}
            # probabilities.append(new_element)
            probabilities_1.append(a2)
            probabilities_2.append(Candidate_Substitutes[i])
            Rank.append([Candidate_Substitutes[i], material[i], a2[0][0]])
        Rank.pop(0)
        for s1 in range(len(Rank)-1,0,-1):
            for s2 in range(s1):
                if Rank[s2][2]<Rank[s2+1][2]:
                    temp = Rank[s2]
                    Rank[s2] = Rank[s2+1]
                    Rank[s2+1] = temp
        print(Rank)
        with open("/home/nithin/Desktop/ThreeDCV/Research/Material_Prop/Results_HIT.csv", "a") as output:
            output.write("\n")
            output.write(filename)
            output.write("\n")
            writer = csv.writer(output, lineterminator='\n')
            writer.writerows(Rank)
