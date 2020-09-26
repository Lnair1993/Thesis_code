% Attachment point transformation based on relative position to mean
% Prespecify point clouds with centered or end attachments

function att_tf = att_point_tfm(match, pcl)    
    pcl_mean = mean(pcl.Location);
    att_temp_min = min(pcl.Location);
    att_temp_max = max(pcl.Location);
    
    if match == "inputCloud1.ply" || match == "inputCloud2.ply" || match == "inputCloud3.ply"
        att_tf = pcl_mean; %Middle
    elseif match == "inputCloud10.ply" %Spatula
        att_tf = [att_temp_max(1), pcl_mean(2), pcl_mean(3); pcl_mean];
    elseif match == "inputCloud7.ply" || match == "inputCloud8.ply" %Cylindrical spatula handle or spoon
        att_tf = [att_temp_max(1), pcl_mean(2), pcl_mean(3); att_temp_min(1), pcl_mean(2), pcl_mean(3)];
    elseif match == "inputCloud5.ply" %No attachments
        att_tf = [inf, inf, inf];
    else
        att_tf = [att_temp_min(1), pcl_mean(2), pcl_mean(3)]; %End point
    end
end