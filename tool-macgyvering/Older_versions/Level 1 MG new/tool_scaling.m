%% Take in a tool category and rescale the input tool point cloud
% Input: Point cloud of tool, tool category
% Output: scaled point cloud, scaling factor

function [new_tool_pcl, mult_rescale] = tool_scaling(tool_category, tool_pcl) 
    
    old_scale = range(tool_pcl.Location);

    switch tool_category
        case 'breadknife'
            max_size = 0.3;
        case 'bowl'
            max_size = 0.2;
        case 'chineseknife'
            max_size = 0.35;
        case 'chopstick'
            max_size = 0.2;     
        case 'knifechinese'
            max_size = 0.35;
        case 'fryingpan'
            max_size = 0.5;
        case 'fork'
            max_size = 0.3;
        case 'hammer'
            max_size = 0.4;
        case 'kitchenknife'
            max_size = 0.3;
        case 'tableknife'
            max_size = 0.25;
        case 'ladle'
            max_size = 0.15;
        case 'mallet'
            max_size = 0.4;
        case 'meshspatula'
            max_size = 0.4;
        case 'mug'
            max_size = 0.15;
        case 'pencil'
            max_size = 0.2;
        case 'pen'
            max_size = 0.2;
        case 'rollingpin'
            max_size = 0.4;
        case 'servingspoon'
            max_size = 0.4;
        case 'skillet'
            max_size = 0.4;
        case 'spatula'
            max_size = 0.3;
        case 'tablespoon'
            max_size = 0.25;
        case 'squeegee'
            max_size = 0.2;
        case 'tablefork'
            max_size = 0.25;
        case 'bottle'
            max_size = 0.3;
        case 'vase'
            max_size = 0.4;
        case 'cup'
            max_size = 0.15;
        case 'plate'
            max_size = 0.25;
        case 'spoon'
            max_size = 0.15;
        otherwise
            max_size = 0.5;
            warning(['Could not find tool category ' tool_category]);
    end
    
    mult_rescale = max_size/max(old_scale);
    new_points = mult_rescale*tool_pcl.Location;
    new_tool_pcl = pointCloud(new_points);
end