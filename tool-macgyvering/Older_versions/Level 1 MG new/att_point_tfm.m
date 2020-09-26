% Attachment point transformation based on relative position to mean

function att_tf = att_point_tfm(att_point, obj_pose, pcl_mean)
    att_tf = pcl_mean - obj_pose + att_point;
end