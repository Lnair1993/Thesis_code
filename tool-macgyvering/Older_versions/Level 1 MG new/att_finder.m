% Function that takes in the point clouds already translated and checks if
% good attachment points for that configuration exist
% It does so by flipping each part and checking for matches - if no matches
% in any configuration, it returns false
% Else, return true with the correct attachment point IDs and poses

function [att_point_IDs] = att_finder(action_scores, grasp_scores, parts_files_list, part_location, input_full_tool_file)

    % Files corresponding to the attachment points and the object positions
    att_point_file = 'attachment_points.csv';
    obj_poses_file = 'Object_positions.csv';
    
    % A counter to check if suitable action and grasp parts have been found
    part_nums = 0;
    
    % Fit scores for different part combinations
    [action_part_idx, grasp_part_idx] = parts_combo(action_scores, grasp_scores);
    % Relative angles and positions for the input/source tool
    [angle_relative, pos_relative] = relative_params(input_full_tool_file);
    
    att_dist = 0.05; %Distance threshold between attachment point and pcl point
    
    % NOTE: Might have to subtract some value from marker pose since the AR Tag
    % is a little faraway from the magnet
    % NOTE: Consider using containers, maps for objects, att points
    
    for i = 1:length(action_part_idx)
        % Retrieve the corresponding action and grasp part pcl files
        
        action_match = parts_files_list(action_part_idx(i),:).name;
        grasp_match = parts_files_list(grasp_part_idx(i),:).name;
        
        % Orient them based on the input/source tool
        [action_pcl_tf, grasp_pcl_tf, min_grasp_x, max_action_x] = parts_orient(action_match, grasp_match, angle_relative, pos_relative, part_location);
        
        % Get the means in this new coordinate frame
        action_mean = mean(action_pcl_tf.Location);
        grasp_mean = mean(grasp_pcl_tf.Location);
            
        % Read attachment points, objects poses for action and grasp parts
        att_points = att_reader(att_point_file);
        obj_pose = obj_pose_reader(obj_poses_file);
        
        action_pose = obj_pose(action_part_idx(i),:);
        grasp_pose = obj_pose(grasp_part_idx(i),:);
            
        att_point_action = att_points(action_part_idx(i),:);
        att_point_grasp = att_points(grasp_part_idx(i),:);
        
        % Attachment point IDs for the specified action, grasp parts
        att_point_action_ID = att_point_action(1);
        att_point_grasp_ID = att_point_grasp(1);
        
        % Remove ID part
        att_point_action_original = att_point_action(2:end);
        att_point_grasp_original = att_point_grasp(2:end);
        
        % Transformed attachment points within new coordinate frame
        % relative to the new mean of the objects
        att_point_action = att_point_tfm(att_point_action_original, action_pose, action_mean);
        att_point_grasp = att_point_tfm(att_point_grasp_original, grasp_pose, grasp_mean);
        
        % Get distance of attachment point from the point cloud attachment
        action_dist = sqrt(sum((att_point_action - max_action_x).^2));
        grasp_dist = sqrt(sum((att_point_grasp - min_grasp_x).^2));
        
        % Check if attachment points exists within close vicinity on action and grasp parts
        if action_dist > att_dist
            % If not, flip the object and repeat the check
            fprintf("Attachment points not found.. flipping object \n");
            action_pcl_tf = pcl_flip(action_pcl_tf);
            action_mean = mean(action_pcl_tf.Location);
            att_point_action = att_point_tfm(att_point_action_original, action_pose, action_mean);
            max_action_pt = max(action_pcl_tf.Location);
            max_action_x = max_action_pt(1);
            action_dist = sqrt(sum((att_point_action - max_action_x).^2));
            if action_dist > att_dist
                % The object does not have suitable attachment points
                fprintf("Action Object with no attachment points \n")
            else
                part_nums = part_nums + 1;
            end
        else
            part_nums = part_nums + 1;
        end
        
        % Repeat above for the grasp parts as well
        if grasp_dist > att_dist
            fprintf("Attachment points not found.. flipping object \n");
            grasp_pcl_tf = pcl_flip(grasp_pcl_tf);
            grasp_mean = mean(grasp_pcl_tf.Location);
            att_point_grasp = att_point_tfm(att_point_grasp_original, grasp_pose, grasp_mean);
            min_grasp_pt = min(grasp_pcl_tf.Location);
            min_grasp_x = min_grasp_pt(1);
            grasp_dist = sqrt(sum((att_point_grasp - min_grasp_x).^2));
            if grasp_dist > att_dist
                fprintf("Grasp Object with no attachment points \n")
                part_nums = 0;
            else
                part_nums = part_nums + 1;
            end
        else
            part_nums = part_nums + 1;
        end
        
        if part_nums == 2 % Suitable action, grasp combo found
            %Visualize the results
            fprintf("Suitable parts found \n");
            action_match
            grasp_match
            figure;
            pcshowpair(action_pcl_tf, grasp_pcl_tf);
            title('Object parts to use');
            xlabel('X')
            ylabel('Y')
            zlabel('Z')
            
            %Return the correct attachment points
            att_point_IDs = [att_point_action_ID, att_point_grasp_ID];
            break;
        end
        
    end
end
        att_point_grasp = att_points(grasp_part_idx(i),:);
        
        % Attachment point IDs for the specified action, grasp parts
        att_point_action_ID = att_point_action(1);
        att_point_grasp_ID = att_point_grasp(1);
        
        % Remove ID part
        att_point_action = att_point_action(2:end);
        att_point_grasp = att_point_grasp(2:end);
        
        % Transformed attachment points within new coordinate frame
        % relative to the new mean of the objects
        att_point_action = att_point_tfm(att_point_action, action_pose, action_mean);
        att_point_grasp = att_point_tfm(att_point_grasp, grasp_pose, grasp_mean);
        
        % Get distance of attachment point from the point cloud attachment
        action_dist = sqrt(sum((att_point_action - max_action_x).^2));
        grasp_dist = sqrt(sum((att_point_grasp - min_grasp_x).^2));
        
        % Check if attachment points exists within close vicinity on action and grasp parts
        if action_dist > att_dist
            % If not, flip the object and repeat the check
            action_pcl_tf = pcl_flip(action_pcl_tf);
            max_action_pt = max(action_pcl_tf.Location);
            max_action_x = max_action_pt(1);
            action_dist = sqrt(sum((att_point_action - max_action_x).^2));
            if action_dist > att_dist
                % The object does not have suitable attachment points
                fprintf("Action Object with no attachment points \n")
            else
                part_nums = part_nums + 1;
            end
        else
            part_nums = part_nums + 1;
        end
        
        % Repeat above for the grasp parts as well
        if grasp_dist > att_dist
            grasp_pcl_tf = pcl_flip(grasp_pcl_tf);
            min_grasp_pt = min(grasp_pcl_tf.Location);
            min_grasp_x = min_grasp_pt(1);
            grasp_dist = sqrt(sum((att_point_grasp - min_grasp_x).^2));
            if grasp_dist > att_dist
                fprintf("Grasp Object with no attachment points \n")
                part_nums = 0;
            else
                part_nums = part_nums + 1;
            end
        else
            part_nums = part_nums + 1;
        end
        
        if part_nums == 2 % Suitable action, grasp combo found
            %Visualize the results
            fprintf("Suitable parts found \n");
%             figure;
%             pcshowpair(action_pcl_tf, grasp_pcl_tf);
%             title('Object parts to use');
%             xlabel('X')
%             ylabel('Y')
%             zlabel('Z')
            
            %Return the correct attachment points
            att_point_IDs = [att_point_action_ID, att_point_grasp_ID];
            break;
        end
        
    end
end
