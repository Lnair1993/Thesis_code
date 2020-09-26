import os, sys
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

## Function to create data pairs
def data_pairs_creation(data, data_pairs, n_classes):
    pairs = []
    index_pairs = []
    labels = []
    count_pos = 0.0
    count_neg = 0.0
    n = [len(data_pairs[d]) for d in range(len(n_classes))]
    for d in range(len(n_classes)):
        for i in range(int(n[d])):
            for j in range(i+1,int(n[d])):
                z1, z2 = data_pairs[d][i], data_pairs[d][j]
                pairs.append([data[z1],data[z2]])
                labels.append(1)
		#count_pos = count_pos + 1
                inc = random.randrange(1, len(n_classes))
                dn = (d+inc)%(len(n_classes))
                if j >= int(n[dn]):
                    continue
                else:
                    z1, z2 = data_pairs[d][i], data_pairs[dn][j]
                    pairs.append([data[z1],data[z2]])
                    index_pairs.append([z1,z2])
                    labels.append(0)
		    #count_neg = count_neg + 1
    return np.array(pairs), np.array(labels)


# object_class = 'cut'
object_class = 'flip'
#object_class = 'hit'
#object_class = 'scoop'
#object_class = 'screw'
#object_class = 'rake'
#object_class = 'squeegee'


materials = ['plastic', 'paper', 'wood', 'metal', 'foam']

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
# print(y_materials2)
# print(y_materials)
# print np.shape(X), np.shape(y_materials), np.shape(y_objects), np.shape(X2), np.shape(y_materials2), np.shape(y_objects2)


X = np.concatenate([X, X2], axis=0)
y_materials = np.concatenate([y_materials, y_materials2], axis=0)
y_objects = np.concatenate([y_objects, y_objects2], axis=0)
wavelengths = np.array(wavelengths)

# MODIFIED - LAKSHMI
#np.save('/home/nithin/Desktop/ThreeDCV/Research/Material_Prop/wavelengths.npy',wavelengths)
#np.save('/home/lnair3/Dual_NN_materials/Wavelengths/wavelengths_' + object_class + '.npy', wavelengths)

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

# print np.shape(X), np.shape(y_materials), np.shape(y_objects)

# ## Metal Indices
# metal_indices = [i for i,x in enumerate(y_objects) if x in metals]
# print(metal_indices)
# # print(y_materials[metal_indices[0]:metal_indices[len(metal_indices)-1]])
# print([x for i,x in enumerate(y_materials) if i in metal_indices])
# ## Wood Indices
# wood_indices = [i for i,x in enumerate(y_objects) if x in woods]
# print(wood_indices)
# print(y_materials[wood_indices[0]:wood_indices[len(wood_indices)-1]])
## Paper Indices
# paper_indices = [i for i,x in enumerate(y_objects) if x in papers]
# print(paper_indices)
# print(y_materials[paper_indices[0]:paper_indices[len(paper_indices)-1]])
# ## Plastic Indices
# plastic_indices = [i for i,x in enumerate(y_objects) if x in plastics]
# print(plastic_indices)
# print(y_materials[plastic_indices[0]:plastic_indices[len(plastic_indices)-1]])
## Foam Indices
# foam_indices = [i for i,x in enumerate(y_objects) if x in foam]
# print(foam_indices)
# print(y_materials[foam_indices[0]:foam_indices[len(foam_indices)-1]])

X = util.firstDeriv(X, wavelengths)
Y = np.array(y_materials)

X_test = util.firstDeriv(X_new_test, wavelengths)
print(X_test.shape)
Y_test = np.array(y_materials_new_test)
print(Y_test)

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
elif object_class == 'screw':
    Y_test[Y_test==6] = 1
    Y_test[Y_test==7] = 0
    Y_test[Y_test==8] = 0
    Y_test[Y_test==9] = 1
    Y_test[Y_test==10] = 0
    print(Y)
    print("screw")
    Y[Y==6] = 1
    Y[Y==7] = 0
    Y[Y==8] = 0
    Y[Y==9] = 1
    Y[Y==10] = 0
    print(Y)
    print("screw")
elif object_class == 'rake':
    Y_test[Y_test==6] = 1
    Y_test[Y_test==7] = 0
    Y_test[Y_test==8] = 1
    Y_test[Y_test==9] = 1
    Y_test[Y_test==10] = 0
    print(Y)
    print("rake")
    Y[Y==6] = 1
    Y[Y==7] = 0
    Y[Y==8] = 1
    Y[Y==9] = 1
    Y[Y==10] = 0
    print(Y)
    print("rake")
elif object_class == 'squeegee':
    Y_test[Y_test==6] = 0
    Y_test[Y_test==7] = 0
    Y_test[Y_test==8] = 0
    Y_test[Y_test==9] = 0
    Y_test[Y_test==10] = 1
    print(Y)
    print("squeegee")
    Y[Y==6] = 0
    Y[Y==7] = 0
    Y[Y==8] = 0
    Y[Y==9] = 0
    Y[Y==10] = 1
    print(Y)
    print("squeegee")

# X,Y = shuffle(X,Y,random_state=1)
# X_train, X_test, Y_train, Y_test = train_test_split(X,Y,test_size=0.1,random_state=1)

## Preprocessing
scaler = StandardScaler()
scaler.fit(X)
X = scaler.transform(X)
X_test = scaler.transform(X_test)
input_shape = X.shape[1:]

## Save the StandardScaler object for use during testing
# MODIFIED - LAKSHMI
#scaler_filename = '/home/nithin/Desktop/ThreeDCV/Research/Material_Prop/scaler_materials_scoop.save'
scaler_filename = '/home/lnair3/Dual_NN_materials/Scalar_wts/scaler_materials_' + object_class + '.save'

joblib.dump(scaler, scaler_filename)

## Create the Training and Testing Pairs
n_classes,_ = np.unique(Y, return_counts=True, axis=0)

training_pairs = [np.where(Y==i)[0] for i in n_classes]
x_train, y_train = data_pairs_creation(X, training_pairs, n_classes)
x_train, y_train = shuffle(x_train, y_train,random_state=1)

testing_pairs = [np.where(Y_test==i)[0] for i in n_classes]
x_test, y_test = data_pairs_creation(X_test, testing_pairs, n_classes)

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
# model.load_weights("/home/nithin/Desktop/ThreeDCV/Research/Material_Prop/CUT_L2/material_prop_weights_flip.h5")
#
# layer_dict = dict([(layer.name, layer) for layer in model.layers])
# weights_fusion_layer = layer_dict['Fusion'].get_weights()
# weights_final_layer = layer_dict['Final_Layer'].get_weights()
# weights_fusion_layer = np.array(weights_fusion_layer)
# weights_final_layer = np.array(weights_final_layer)
#
#
# old_tool_encoding_full = np.load("/home/nithin/Desktop/ThreeDCV/Research/Material_Prop/CUT_L2/embeddings_material_prop_flip.npy")
# print(old_tool_encoding_full.shape)
# old_tool_encoding = np.mean(old_tool_encoding_full,axis=0)
# old_tool_encoding = old_tool_encoding.reshape(old_tool_encoding.shape[0],1)
# print(old_tool_encoding.shape)
#
# for x in X_test:
#     tool_features = x.reshape((1,331))
#     new_tool_encoding = base_network.predict(tool_features)
#     l1_distance_new_layer = np.absolute(new_tool_encoding.T-old_tool_encoding)
#     z1 = np.dot(l1_distance_new_layer.T,weights_fusion_layer[0]) + weights_fusion_layer[1]
#     a1 = np.maximum(z1,0)
#     z2 = np.dot(a1,weights_final_layer[0]) + weights_final_layer[1]
#     a2 = sigmoid(z2)
#     print(a2)


model.fit([x_train[:,0], x_train[:,1]], y_train, validation_split=0.2, epochs=10, batch_size=30, verbose=2)

# MODIFIED - LAKSHMI
#model.save('/home/lnair3/Dual_NN_materials/Model/material_prop_' + object_class + '.h5')
#model.save_weights('/home/lnair3/Dual_NN_materials/Model/material_prop_weights_' + object_class + '.h5')

#model.save('/home/nithin/Desktop/ThreeDCV/Research/Material_Prop/material_prop_scoop.h5')
#model.save_weights('/home/nithin/Desktop/ThreeDCV/Research/Material_Prop/material_prop_weights_scoop.h5')

plot_model(model,to_file='model.png')
print(model.summary())
print(base_network.summary())
results = model.predict([x_test[:,0], x_test[:,1]])
for i in range(results.shape[0]):
    if results[i]>=0.5:
        results[i] = 1
    else:
        results[i] = 0
results = results.flatten()
print(results)
print(y_test)
print(classification_report(y_test,results))
print(confusion_matrix(y_test,results))

## Create Embeddings
embedding_data = np.copy(X)
embedding_data_label = np.copy(Y)
embedding_data_indices = [i for i,x in enumerate(embedding_data_label) if x == 1]
embedding_inputs = [x for i,x in enumerate(embedding_data) if i in embedding_data_indices]
embedding_inputs = np.array(embedding_inputs)
embedding_outputs = base_network.predict(embedding_inputs)
print(embedding_outputs.shape)

# MODIFIED - LAKSHMI
#np.save('/home/lnair3/Dual_NN_materials/embeddings_material_prop_' + object_class + '.npy', embedding_outputs)
#np.save('/home/nithin/Desktop/ThreeDCV/Research/Material_Prop/embeddings_material_prop_scoop.npy',embedding_outputs)
