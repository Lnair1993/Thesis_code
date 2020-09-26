% Flip point cloud about its mean point

function flipped_pcl = pcl_flip(pcl)
    % Move object to origin
    pcl_mean = mean(pcl.Location);
    tform = makehgtform('translate', -pcl_mean);
    tform = affine3d(tform');
    pcl_tf = pctransform(pcl, tform);
    
    % Rotate 180 degrees about the Z axis
    tform = makehgtform('zrotate', pi);
    tform = affine3d(tform');
    pcl_tf = pctransform(pcl_tf, tform);
    
    % Move back to original mean
    tform = makehgtform('translate', pcl_mean);
    tform = affine3d(tform');
    flipped_pcl = pctransform(pcl_tf, tform);
    
end