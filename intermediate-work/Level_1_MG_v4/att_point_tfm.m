% Attachment point transformation based on relative position to mean
% Prespecify point clouds with centered or end attachments

function att_tf = att_point_tfm(match, pcl)    
    pcl_mean = mean(pcl.Location);
    att_temp_min = min(pcl.Location);
    att_temp_max = max(pcl.Location);
    
    if contains(match, "wood_long_midPoint") || contains(match, "wood_short_midPoint") || contains(match, "wood_L_shape") || contains(match, "red_flat_piece_1mag")
        att_tf = pcl_mean; %Middle
    elseif contains(match, "red_flat_piece_2mag") %Spatula
        att_tf = [att_temp_max(1), pcl_mean(2), pcl_mean(3); pcl_mean];
    elseif contains(match, "red_cylinder_magnetic") || contains(match, "steel_bowl_small") %Cylindrical spatula handle or spoon
        att_tf = [att_temp_max(1), pcl_mean(2), pcl_mean(3); att_temp_min(1), pcl_mean(2), pcl_mean(3)];
    elseif contains(match, "wood_long_endPoint")
        att_tf = [att_temp_min(1), pcl_mean(2), pcl_mean(3)]; %End point
    else
        att_tf = [];
    end
end