%% Perform matching from one point cloud to another
% Input - sample and reference point clouds
% Output - fitting score

function [score] = projection(sample, reference)
    pcl_template = sample;
    angles = [pi/6, pi/3, pi/2, pi, 3*pi/2];
    residue_opt = 1000;

    for i = 1:size(angles,2)
        R = makehgtform('xrotate',0,'yrotate',0,'zrotate',angles(i));
        pcl_temp = pctransform(pcl_template, affine3d(R));
        [~,~, residue] = pcregrigid(pcl_temp, reference, 'Metric','pointToPlane','Extrapolate', true);
        if residue < residue_opt
            residue_opt = residue;
        end
    end
    
    score = residue_opt;
    
end