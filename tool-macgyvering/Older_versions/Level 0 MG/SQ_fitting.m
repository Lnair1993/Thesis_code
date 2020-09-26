%% Superellipsoid fitting to tool parts based on Abelha 2016
% 1) No bending or tapering parameters implemented yet 

% Input: "SEGMENTED" point cloud - currently using the Tool-Web dataset,
% type of SQ to fit
% Output: Best fit superquadrics 3D points

function [SQ_out] = SQ_fitting(point_cloud, SQ_type)
    %% Analyze segments
    [segments, num_segments] = segment_return(point_cloud);

    % Initialize optimum SQ parameters for each pcl segment that is fitted to
    SQ_optimum = zeros(num_segments, 12); %12 for toroids, 11 for others
    optimum_type = zeros(1,num_segments);

    %% Fit segments using non-linear optimizations

    pcld_location = point_cloud.Location;
    pcl_tform = [];

    inv_pca_optimum = zeros(num_segments, 9);

    for i = 1:num_segments
        residue_SQ = 1000;

        % Find members of each segment
        segment_indices = find(segments == i);
        segment_members = pcld_location(segment_indices,:);
        segment_original = segment_members;

        % Save the original segment pose
        pcl_tform = vertcat(pcl_tform, segment_members);

        % Get segment transformed using PCA and the inverse transformation
        [segment_members, inv_pca] = pca_segment(segment_members);
        inv_pca_optimum(i,:) = reshape(inv_pca,[1,9]);

        for j = 1:size(SQ_type,2)
            type = SQ_type(j);

            % Parameter Initialization for the segment
            [scale, orientations, eps, p, bound_min, bound_max] = param_init(segment_members, type);

            % Min and Max bounds for optimization based on the initial parameters
            min_bound = double([0.8*scale(1), 0.8*scale(2), 0.8*scale(3), 0.01, 0.1, 0.1,...
                -pi, -pi, -pi, bound_min(1), bound_min(2), bound_min(3)]);
            max_bound = double([1.2*scale(1), 1.2*scale(2), 1.2*scale(3), 1, 2.0, 2.0,...
                pi, pi, pi, bound_max(1), bound_max(2), bound_max(3)]); 

            % Initialize the 12 parameters for superquadrics
            x_init = double([scale(1), scale(2), scale(3), scale(4), eps(1),...
                eps(2), orientations(1), orientations(2), orientations(3),...
                p(1), p(2), p(3)]);

            % Levenberg-Marquardt optimization
            options = optimset('Display','off','TolX',1e-10,'TolFun',1e-10,'MaxIter',3000,'MaxFunEvals',3000); 
            [optimum_quadrics,~,~,~,~] = lsqnonlin(@(x) fitting_fn(x,segment_members,type), x_init, min_bound, max_bound, options);
            %optimum_quadrics = x_init;

            % Ranking the SQs
            SQ = SQ2PCL(optimum_quadrics, type);
            SQ = SQ*inv_pca;
            [pcl_SQ_dist, SQ_pcl_dist] = pcl_dist(segment_original, SQ);
            residue = pcl_SQ_dist + SQ_pcl_dist;

            if residue < residue_SQ
                SQ_optimum(i,:) = optimum_quadrics;
                residue_SQ = residue;
                optimum_type(i) = type;
            end
        end
    end

    %% Point cloud for optimum Superquadric

    SQ_tform = [];

    for i = 1:num_segments
        % Generate a SQ pcl from optimum_quadrics and apply inverse pca tform
        SQ = SQ2PCL(SQ_optimum(i,:), optimum_type(i));
        %fprintf("Optimum type is %d \n", optimum_type(i));
        inv_pca = reshape(inv_pca_optimum(i,:),[3,3]);
        SQ = SQ*inv_pca;

        % Save the transformed SQ (coordinate frame of original PCL)
        SQ_tform = vertcat(SQ_tform, SQ);
    end

    %visualize_SQ(SQ_tform, pcl_tform);
    SQ_out = SQ_tform;
end
