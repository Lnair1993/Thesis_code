%Create a new folder with all segmented point clouds

fileFolder = '/home/lnair3/RAIL_codebase/lnair3/Segment_extract/segment_object';
filepath = fullfile(fileFolder,'*.ply');
fileList = dir(filepath);

for i = 1:length(fileList)
    filename = fileList(i).name;
    point_cloud = pcread(fullfile(fileFolder,filename));
    
    [segments, num_segments] = segment_return(point_cloud);
    pcld_location = point_cloud.Location;
    
    for j = 1:num_segments
        segment_indices = find(segments == j);
        segment_members = pcld_location(segment_indices,:);
        segment_pcl = pointCloud(segment_members);
        segment_file = strjoin([strtok(filename,'.'),j,".ply"],'');
        pcwrite(segment_pcl, segment_file);
    end
end