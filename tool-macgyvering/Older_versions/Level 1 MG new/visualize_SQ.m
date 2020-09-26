%% Visualizing 2 point clouds together
% Input - the 2 point clouds
% Output - visualization

function [] = visualize_SQ(SQ_tform, pcl_tform)

point_cloud = pointCloud(pcl_tform);
pcl_SQ = pointCloud(SQ_tform);

figure;
pcshowpair(pcl_SQ, point_cloud);
xlabel('X')
ylabel('Y')
zlabel('Z')

end