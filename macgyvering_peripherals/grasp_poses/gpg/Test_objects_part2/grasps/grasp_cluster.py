import csv
import ast
import numpy as np

from scipy.cluster.hierarchy import fclusterdata

file_in = "test_object_grasps.csv"
file_out = "objects_grasp_cluster.csv"

# Read grasps for each point cloud
# Cluster points that are within some distance threshold
# Save clustered grasp points into another file

grasps = {}
object_centroids = {}
grasp_clustered = {}

with open(file_in, 'r') as file_in:
    reader = csv.reader(file_in)
    reader.next()
    for row in reader:
        pcl_name = row[0]
        pcl_centroid = ast.literal_eval(row[1])
        object_grasps = ast.literal_eval(row[2])

        grasps[pcl_name] = object_grasps
        object_centroids[pcl_name] = pcl_centroid

dist_threshold = 0.1

for key in grasps.keys():
    grasp_pts = grasps[key]
    if len(grasp_pts) > 1:
        cluster_idx = fclusterdata(np.array(grasp_pts), dist_threshold)
        tested_idx = []
        grasp_final = []
        for i, item in enumerate(grasp_pts):
            if cluster_idx[i] not in tested_idx:
                tested_idx.append(cluster_idx[i])
                grasp_final.append(item)
        grasp_clustered[key] = grasp_final
    else:
        grasp_clustered[key] = grasp_pts

grasp_data_final = []

for key in grasps.keys():
    value = [key, object_centroids[key], grasp_clustered[key]]
    grasp_data_final.append(value)

with open(file_out, 'w') as file_out:
    writer = csv.writer(file_out)
    writer.writerows(grasp_data_final)
    

