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

    object_class = 'rake'
    object_class = 'flip'
    object_class = 'scoop'
    object_class = 'screw'
    object_class = 'hit'
    object_class = 'squeegee'

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
