% Given action, grasp part point clouds, transform their relative
% positioning to match that of the source tool

function [action_pcl_tf, grasp_pcl_tf, min_grasp_x, max_action_x] = parts_orient(action_match, grasp_match, angle_relative, pos_relative, part_location)

    action_object = pcread(fullfile(part_location, action_match));
    grasp_object = pcread(fullfile(part_location, grasp_match));
    
    %NEED TO FLATTEN BOTH PARTS ALONG XY PLANE
    
    tform_action = makehgtform('translate', -mean(action_object.Location));
    tform_action = affine3d(tform_action');
    action_object = pctransform(action_object, tform_action);

    max_action_pt = max(action_object.Location);
    max_action_x = max_action_pt(1);

    tform_grasp = makehgtform('translate', -mean(grasp_object.Location)+pos_relative);
    tform_grasp = affine3d(tform_grasp');
    grasp_object = pctransform(grasp_object, tform_grasp);

    min_grasp_pt = min(grasp_object.Location);
    min_grasp_x = min_grasp_pt(1);

    if min_grasp_x > max_action_x
        diff = min_grasp_x - max_action_x; % Towards origin - max_action_x and min_grasp_x is the att_point
    elseif min_grasp_x < max_action_x
        diff = max_action_x - min_grasp_x; % Away from origin - min_action_x
    end

    tform_grasp = makehgtform('translate', [diff,0,0], 'xrotate', angle_relative(1), ...
         'yrotate', angle_relative(2), 'zrotate', angle_relative(3));
    tform_grasp = affine3d(tform_grasp');
    grasp_object = pctransform(grasp_object, tform_grasp);

    action_pcl_tf = action_object;
    grasp_pcl_tf = grasp_object;

end
