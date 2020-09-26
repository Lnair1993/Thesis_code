%% Level 1 MACGYVERING - WITH ATTACHMENT POINTS
% Create composite objects from individual parts to match a source tool

%TO DO:
% - Transform part point clouds to XY plane for easy flipping about Z axis
% - Multiple attachment points incorporated
% - Using maps, containers for object pose and attachment points relations
% - Overall code debugging and logic verification, more testing
% - Incorporate attachment point absence into parts score (high penalty for
% no attachment points)
% - Incorporate improved fitting code
% - Separate action and grasp parts

% Specify location of individual parts point clouds

part_location = '/home/lnair3/Github files/lnair3/Macgyvering/Level 1 MG new/Segment_parts';
parts_path = fullfile(part_location,'*.ply');
file_list = dir(parts_path);

input_full_tool_file = 'hammer_8_3dwh.ply';
%input_full_tool_file = 'spoon_1_3dwh.ply';

input_tool_action_file = 'hammer_8_3dwh1.ply';
%input_tool_action_file = 'spoon_1_3dwh2.ply';
input_tool_action = pcread(input_tool_action_file);

mean_pos_action = mean(input_tool_action.Location);
pca_pcl = pca(input_tool_action.Location);
angle_action = rotm2eul(pca_pcl);

input_tool_grasp_file = 'hammer_8_3dwh2.ply';
%input_tool_grasp_file = 'spoon_1_3dwh1.ply';
input_tool_grasp = pcread(input_tool_grasp_file);

mean_pos_grasp = mean(input_tool_grasp.Location);
pca_pcl = pca(input_tool_grasp.Location);
angle_grasp = rotm2eul(pca_pcl);

% Rescale the point clouds depending on category
tool_cat = strtok(input_tool_action_file,'_');
[input_tool_action, ~] = tool_scaling(tool_cat, input_tool_action);
[input_tool_grasp, ~] = tool_scaling(tool_cat, input_tool_grasp);

SQ_type_action = 0; %Known type of SQ given as input
SQ_type_grasp = 0;

figure;
pcshow(input_full_tool_file);
title('Input tool')

%% Fit SQ to each segment

[action_params, action_fit_type, action_part_pcl, action_res] = SQ_fitting_params(input_tool_action, SQ_type_action);
action_res;

if action_fit_type == 2
    action_scale = action_params(1:4);
else
    action_scale = action_params(1:3);
end

[grasp_params, grasp_fit_type, grasp_part_pcl, grasp_res] = SQ_fitting_params(input_tool_grasp, SQ_type_grasp);
grasp_res;

if grasp_fit_type == 2
    grasp_scale = grasp_params(1:4);
else
    grasp_scale = grasp_params(1:3);
end

fixture_type = 'fixed'; % Ignore fixture type for now 

figure;
pcshowpair(action_part_pcl, input_tool_action);
title('Action Part');
xlabel('X');
ylabel('Y');
zlabel('Z');

figure;
pcshowpair(grasp_part_pcl, input_tool_grasp);
title('Grasp Part');
xlabel('X');
ylabel('Y');
zlabel('Z');

% Sort dimensions
[~,action_idx] = sort(action_scale,'descend');
[~,grasp_idx] = sort(grasp_scale,'descend');

%% ACTION, GRASP MATCH

action_scores = zeros(1,length(file_list));
grasp_scores = zeros(1,length(file_list));

filenames_ranked = zeros(1,length(file_list));

if SQ_type_action == 2
    ranked_action_params = zeros(length(file_list),12);
else
    ranked_action_params = zeros(length(file_list),11);
end

if SQ_type_grasp == 2
    ranked_grasp_params = zeros(length(file_list),12);
else
    ranked_grasp_params = zeros(length(file_list),11);
end

for i = 1:length(file_list) % Read each segment file
    filename = file_list(i).name;
    fprintf(filename+"\n");
    point_cloud = pcread(fullfile(part_location,filename));
    
    % Rescale each part
    tool_cat = strtok(filename,'_');
    [point_cloud, part_scale] = tool_scaling(tool_cat, point_cloud);
    
    
    [action_SQ_params, ~, SQ_action_subs, residue_action] = SQ_fitting_params(point_cloud, SQ_type_action);    
    score_action = residue_action;
    
 
    [grasp_SQ_params, ~, SQ_grasp_subs, residue_grasp] = SQ_fitting_params(point_cloud, SQ_type_grasp);    
    score_grasp = residue_grasp;  
    
    ranked_action_params(i,:) = action_SQ_params;
    ranked_grasp_params(i,:) = grasp_SQ_params;
    action_scores(i) = score_action;
    grasp_scores(i) = score_grasp;
    
end

%% FIND IF ATTACHMENT POINTS EXIST, RETURN ATT POINT IDS AND FINAL POINT CLOUD

% action_scale and grasp_scale


[ranked_score_new, action_part_idx, grasp_part_idx, action_att_points, grasp_att_points] = att_finder(action_scores, grasp_scores, file_list, part_location, input_full_tool_file, action_scale, grasp_scale, ranked_action_params, ranked_grasp_params)
