from sklearn.decomposition import PCA
from matplotlib import pyplot as plt

import csv

# LDA has to be done independently for the different classes (for binary classification problem)

csv_file = 'ShotC_descriptors_attachment.csv'
csv_file_reduced = 'ShotC_reduced.csv'
data = []
labels = []

# Read the features file
with open(csv_file) as csvfile:
    reader = csv.reader(csvfile)
    next(reader, None)
    for row in reader:
        labels.append(row[0])
        feats = row[1:len(row)-1]
        feats = map(float, feats)
        data.append(feats)

reduction_type = 'PCA'
pca_threshold = 0.95

print "Number of feats before reduction: " + str(len(data[0])) + "\n"

if reduction_type == 'PCA':
    percent_variance = []
    n_components = range(2,350)
    pca_flag = True
    for i in n_components:
        pca = PCA(n_components=i)
        pca.fit(data)
        percent_variance.append(sum(pca.explained_variance_ratio_))

        if (sum(pca.explained_variance_ratio_) >= pca_threshold) and pca_flag:
            n_components_final = i
            pca_flag = False

    # Fit data with best PCA
    pca = PCA(n_components=n_components_final)
    pca.fit(data)
    data = pca.transform(data)
    data = zip(labels, data)
    data = [[elt[0]]+list(elt[1]) for elt in data]

    # PCA number of components to percent variance explained graph
    plt.plot(n_components, percent_variance)
    plt.show()

print "Number of feats after reduction: " + str(len(data[0])-1)

with open(csv_file_reduced, 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(data)
