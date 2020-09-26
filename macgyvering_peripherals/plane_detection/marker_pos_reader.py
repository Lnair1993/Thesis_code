#Read the marker positions and ID's from a marker pos file returned by the ALVAR ROS package
#Currently ignoring the orientation of the markers but can potentially be used to guide the robot movement

import csv
import ast
import math

filename_marker = 'marker_pose.csv'
filename_obj = 'Object_positions.txt'
file_out = 'attachment_points.csv'

num_markers = 4
i = 0
count = 0

marker_pos = {}

with open(filename_marker) as f:
	for line in f:
		field = line.split()

		#Save marker ID
		if 'id:' in field:
			object_id = int(field[1])
			count = 0
			poses = [0,0,0]

		#Save marker positions but not orientations 	
		if 'x:' in field and count != 3:
			poses[0] = float(field[1])
			count += 1
		elif 'y:' in field and count != 3:
			poses[1] = float(field[1])
			count += 1
		elif 'z:' in field and count != 3:
			poses[2] = float(field[1])
			count += 1
			marker_pos[object_id] = poses
			i += 1	

		#Save data for all N markers	
		if i == 4:
			break			

object_poses = []
sorted_markers = {}

with open(filename_obj) as f:
	for line in f:
		r = line.split()
		r = ast.literal_eval(r[0])
		object_poses.append(list(r))

for index, obj in enumerate(object_poses):
	dist_best = 10000;
	for marker_id in marker_pos.keys():
		pose = marker_pos[marker_id]
		dist = math.sqrt((obj[0]-pose[0])**2 + (obj[1]-pose[1])**2 + (obj[2]-pose[2])**2)
		if dist < dist_best:
			dist_best = dist
			best_marker_id = marker_id
			best_marker_pose = pose

	sorted_markers[index] = [best_marker_id, best_marker_pose[0], best_marker_pose[1], best_marker_pose[2]]

print sorted_markers
		#Compare each of them to the object_pose file to find closest match 
		#Reoder the attachment points such that they correspond to the point cloud ordering
		#Save the attachment points to another file
with open(file_out, "w") as output:
	writer = csv.writer(output, lineterminator='\n')
	for marker in sorted_markers.values():
		writer.writerow(marker) 



