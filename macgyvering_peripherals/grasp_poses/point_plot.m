input_cloud = 'inputCloud3.ply';

centroid = [0.146369, -0.216099, 1.2179];

grasp_1_bottom = [0.110621, -0.225776, 1.22182];
grasp_1_top = [0.148838, -0.214497, 1.22532];
grasp_1 = vertcat(grasp_1_bottom, grasp_1_top);

grasp_2_bottom = [0.175241, -0.191496, 1.18775];
grasp_2_top = [0.163791, -0.229773, 1.18972];
grasp_2 = vertcat(grasp_2_bottom, grasp_2_top);

pcl_input = pcread(input_cloud);
pcshow(pcl_input);

%hold on;
%scatter3(grasp_1(:,1), grasp_1(:,2), grasp_1(:,3), 'filled');

%hold on;
%scatter3(sum(grasp_1(:,1))/2, sum(grasp_1(:,2))/2, sum(grasp_1(:,3))/2, 'filled');

pt = [0.149092 -0.219353   1.20375];

hold on;
scatter3(pt(1), pt(2), pt(3));


