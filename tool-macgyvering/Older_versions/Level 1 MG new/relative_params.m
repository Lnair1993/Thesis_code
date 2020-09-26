%Given input tool file, retrieve relative parts orientation for the tool

function [angle_relative, pos_relative] = relative_params(input_full_tool_file)
    input_full_tool = pcread(input_full_tool_file);
    tool_cat = strtok(input_full_tool_file,'_');
    [input_full_tool, ~] = tool_scaling(tool_cat, input_full_tool);
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
end