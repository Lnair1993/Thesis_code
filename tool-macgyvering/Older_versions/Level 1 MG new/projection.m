%% Perform matching from one point cloud to another
% Input - sample and reference point clouds
% Output - fitting score

function [score] = projection(sample, reference)
    pcl_template = sample;
    angles = [0, pi/6, pi/3, pi/2, pi, 3*pi/2, -pi/6, -pi/3, -pi/2, -pi, -3*pi/2];
    residue_opt = 1000;

    for k = 1:3
        for i = 1:size(angles,2)
            if k == 1
                R = makehgtform('xrotate',0,'yrotate',0,'zrotate',angles(i));
            elseif k == 2
                R = makehgtform('xrotate',0,'yrotate',angles(i),'zrotate',0);
            else
                R = makehgtform('xrotate',angles(i),'yrotate',0,'zrotate',0);
            end
            pcl_temp = pctransform(pcl_template, affine3d(R));
            [~, ~, residue] = pcregrigid(pcl_temp, reference, 'Extrapolate', true);
            if residue < residue_opt
                residue_opt = residue;
            end
        end
    end
    score = residue_opt;
    
end