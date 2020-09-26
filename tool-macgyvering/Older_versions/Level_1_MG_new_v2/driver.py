import matlab.engine
import time

eng = matlab.engine.start_matlab()

input_tool_full = 'hammer_8_3dwh.ply'
input_action = 'hammer_8_3dwh1.ply'
input_grasp = 'hammer_8_3dwh2.ply'


start = time.time()
#[ranked_score_new, action_part_idx, grasp_part_idx, action_att_points, grasp_att_points] 
answer = eng.MG_lvl_1(input_tool_full, input_action, input_grasp)
end = time.time()

print answer

'''print "Final errors: " + ranked_score_new + "\n"
print "Action part indices: " + action_part_idx + "\n"
print "Grasp part indices: " + grasp_part_idx + "\n"
print "Action part attachments: " + action_att_points + "\n"
print "Grasp part attachments: " + grasp_att_points + "\n"
print "Total computation time: " + (end-start) + "\n"

print "*****************************************************"'''

#Call the plane segmentation function to return the object positions file - also add a verification step so that the user can verify if necessary, the quality of point cloud seg
#Create a dict corresponding to object positions, ID, attachment point locations
#Call tf_listener for object point locations in robot base frame
#Pass the output goal locations to nimbus_move2pose
#If failed Macgyver testing, call next object location

#Later step: Call the AR tag retrieval function for retrieving the positions of the AR tags along with the corresponding object point cloud locations
