%% Level 1 MACGYVERING
% Create composite objects from individual parts to match a source tool

% Upcoming developments:
% - Paraboloid fitting needs fixing 
% - Speed can be improved by dowsampling large point clouds

% Specify location of individual parts point clouds
part_location = 'C:\..';
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

% Task function socring - 'Quad' = 40*scale^2 or 'Lin' = 0.1
% Apply scoring from biggest to smallest dimension
task_func_action = [40,1,1]; 
task_func_grasp = [40,1,1];  

% Task functions for some tools - action, grasp
%[1,40,40],[1,1,1] -> spoon
%[40,1,1],[40,1,1] -> mallet
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

%% Find best combination of objects
[action_part_idx, grasp_part_idx] = parts_combo(action_scores, grasp_scores, action_scale, grasp_scale, ranked_action_params, ranked_grasp_params, action_idx, grasp_idx, task_func_action, task_func_grasp);
action_SQ_params = ranked_action_params(action_part_idx,:);
grasp_SQ_params = ranked_grasp_params(grasp_part_idx,:);

action_match = file_list(action_part_idx).name;
grasp_match = file_list(grasp_part_idx).name;

fprintf("action_match %s \n", action_match);
fprintf("grasp_match %s \n", grasp_match);

figure;
pcshow(fullfile(part_location, action_match));
title('Action Part Match');

figure;
pcshow(fullfile(part_location, grasp_match));
title('Grasp Part Match');

%% Transform individual parts - works for end to end connections

input_full_tool = pcread(input_full_tool_file);
tool_cat = strtok(input_full_tool_file,'_');
[input_full_tool, sc_factor_full] = tool_scaling(tool_cat, input_full_tool);
[segments_full, num_segments] = segment_return(input_full_tool);
angle_relative = zeros(1,3);
pos_relative = zeros(1,3);

for i = 1:num_segments
    pt_location = input_full_tool.Location;
    pt_idx = find(segments_full == i);
    pt_location = pt_location(pt_idx,:);
    angles = pca(pt_location);
    angles = rotm2eul(angles);
    angle_relative = angles - angle_relative;
    pos = mean(pt_location);
    pos_relative = pos-pos_relative;
end

action_object = pcread(fullfile(part_location, action_match));
grasp_object = pcread(fullfile(part_location, grasp_match));

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
    diff = min_grasp_x - max_action_x; % Towards origin 
elseif min_grasp_x < max_action_x
    diff = max_action_x - min_grasp_x; % Away from origin
end

tform_grasp = makehgtform('translate', [diff,0,0], 'xrotate', angle_relative(1), ...
     'yrotate', angle_relative(2), 'zrotate', angle_relative(3));
tform_grasp = affine3d(tform_grasp');
grasp_object = pctransform(grasp_object, tform_grasp);

pcshowpair(action_object, grasp_object)
s = sprintf(['Macgyvered object for ', input_full_tool_file]);
title(s);
xlabel('X')
ylabel('Y')
zlabel('Z')
