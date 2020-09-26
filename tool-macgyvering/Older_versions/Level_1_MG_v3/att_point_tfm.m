% Attachment point transformation based on relative position to mean
% Prespecify point clouds with centered or end attachments

function att_tf = att_point_tfm(match, pcl)    
    pcl_mean = mean(pcl.Location);
    
    if match == "inputCloud1.ply" || match == "inputCloud2.ply" || match == "inputCloud3.ply" || match == "inputCloud8.ply"
        att_tf = pcl_mean;
    else
        att_temp = min(pcl.Location);
        att_tf = [att_temp(1), pcl_mean(2), pcl_mean(3)];
    end
end