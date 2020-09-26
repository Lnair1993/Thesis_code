% Rank combinations of parts based on the fit scores

function [ranked_score_new, action_part_idx, grasp_part_idx] = parts_combo(action_scores, grasp_scores, action_scale, grasp_scale, ranked_action_params, ranked_grasp_params)

% Need to incorporate number of attachment points part
%ranked_score_total = zeros(1,length(action_scores)*(length(grasp_scores)-1));
%size(ranked_score_total)
%action_part_idx = zeros(1,length(ranked_score_total));
%grasp_part_idx = zeros(1,length(ranked_score_total));

ranked_score_total = [];
action_part_idx = [];
grasp_part_idx = [];

relative_scaling = action_scale./grasp_scale;
[relative_scaling,~] = sort(relative_scaling);

for i = 1:length(action_scores)
    for j = 1:length(grasp_scores)
        if j ~= i
            relative_parts_scale = ranked_action_params(i,1:3)./ranked_grasp_params(j,1:3);
            [relative_parts_scale,~] = sort(relative_parts_scale);
            score_total = action_scores(i) + grasp_scores(j) + sqrt(sum((relative_parts_scale - relative_scaling).^2));
            %sum(abs(relative_parts_scale - relative_scaling)); 
            %ranked_score_total(((i-1)*length(grasp_scores))+j) = score_total;
            %action_part_idx(((i-1)*length(grasp_scores))+j) = i;
            %grasp_part_idx(((i-1)*length(grasp_scores))+j) = j;
            ranked_score_total = horzcat(ranked_score_total, score_total);
            action_part_idx = horzcat(action_part_idx, i);
            grasp_part_idx = horzcat(grasp_part_idx, j);
        end
    end
end

[ranked_score_new,ranked_idx] = sort(ranked_score_total);
action_part_idx = action_part_idx(ranked_idx); % Sorted action part indices
grasp_part_idx = grasp_part_idx(ranked_idx); % Corresponding grasp part idx

end
