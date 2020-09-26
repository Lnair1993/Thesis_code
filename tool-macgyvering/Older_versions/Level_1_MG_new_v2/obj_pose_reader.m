% Read and return object positions from given input file

function [object_poses] = obj_pose_reader(filename)
    object_poses = csvread(filename);
end