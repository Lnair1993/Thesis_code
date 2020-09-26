%% TO DO - PRIMARY
% *** Make the longest dimension the z one for ellipsoid!! - knife fitting
%wrong

%% TO DO - SECONDARY
% Better scoring and projection
% Initially assume only 2 segments - action part and grasp part - later
% extend to >2
% First return error if more than 2, next try to combine segments to just 2
% Bending and tapering parameters
% Fix paraboloids part
% Some params not being optimized - eps1 for paraboloid fitting to bowl
% should be = 1.0 for good fit, but at eps1 = 0.01, it doesn't change at
% all

%% Input the desired file from Tool-Web dataset

% filename = 'bottle_1_3dwh.ply'; 
% filename = 'mug_1_3dwh.ply';
% filename = 'hammer_1_3dwh.ply';
% filename = 'bowl_1_3dwh.ply';
% filename = 'chineseknife_1_3dwh.ply';
% filename = 'kitchenknife_1_3dwh.ply';
% filename = 'fyingpan_2_3dwh.ply';

%input_tools = ["bottle_1_3dwh.ply", "mug_1_3dwh.ply", "kitchenknife_1_3dwh.ply"];
%source_tool = 'chineseknife_1_3dwh.ply';

input_tools = ["fyingpan_2_3dwh.ply", "mug_1_3dwh.ply", "bottle_1_3dwh.ply"];
source_tool = 'hammer_1_3dwh.ply';

source_pcl = pcread(source_tool);
SQ_type = [0]; %Ellipsoid - 0, Hyperparaboloid - 1, Toroid - 2, Paraboloid - 3

SQ_source = SQ_fitting(source_pcl, SQ_type);
SQ_source = pointCloud(SQ_source);

errors = zeros(1,size(input_tools,2));

for i = 1:size(input_tools,2)
    fprintf(input_tools(i)+"\n");
    target_pcl = pcread(input_tools(i));
    SQ_target = SQ_fitting(target_pcl, SQ_type);
    SQ_target = pointCloud(SQ_target);
    
    errors(i) = projection(SQ_source, SQ_target);
end

[~,I] = min(errors);
best_tool = input_tools(I(1));

figure;
pcshow(source_tool);
figure;
pcshow(pcread(best_tool));

fprintf("Input tool is " + strtok(source_tool,'_') + "\n");
fprintf("Best match is " + strtok(best_tool,'_') + "\n");