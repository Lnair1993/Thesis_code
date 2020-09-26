% Rank combinations of parts based on the fit scores

function [ranked_score_new, action_part_idx, grasp_part_idx] = parts_combo(action_scores, grasp_scores, action_scale, grasp_scale, ranked_action_params, ranked_grasp_params)

ranked_score_total = [];
action_part_idx = [];
grasp_part_idx = [];

relative_scaling = action_scale./grasp_scale;

%Normalizing the relative scale
relative_scaling = relative_scaling/sum(relative_scaling);

for i = 1:length(action_scores)
    for j = 1:length(grasp_scores)
        if j ~= i
            relative_parts_scale = ranked_action_params(i,1:3)./ranked_grasp_params(j,1:3);
            
            %Normalizing this
            relative_parts_scale = relative_parts_scale/sum(relative_parts_scale);
            
            %score_total = sqrt(sum((relative_parts_scale - relative_scaling).^2)) + action_scores(i) + grasp_scores(j);
            score_total = sum(abs(relative_parts_scale - relative_scaling)) + action_scores(i) + grasp_scores(j);
            
            score_total = score_total + 1*(sum(abs(action_scale - ranked_action_params(i,1:3))) + sum(abs(grasp_scale - ranked_grasp_params(i,1:3))));
            ranked_score_total = horzcat(ranked_score_total, score_total);
            action_part_idx = horzcat(action_part_idx, i);
            grasp_part_idx = horzcat(grasp_part_idx, j);
        end
    end
end

ranked_score_new = ranked_score_total;

end
