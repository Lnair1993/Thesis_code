% Read and return attachment points from specified file
% Attachment abbreviated as att

function [att_points] = att_reader(filename)
    att_points = csvread(filename);
end