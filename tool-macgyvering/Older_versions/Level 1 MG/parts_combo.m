%% Find best combination of individual parts based on their fitting scores and scale differences

function [action_part, grasp_part] = parts_combo(action_scores, grasp_scores, action_scale, grasp_scale, ranked_action_params, ranked_grasp_params, action_idx, grasp_idx, task_func_action, task_func_grasp)

score_opt = inf;
wt_score = 1;
wt_action = 1;
wt_grasp = 1;

for i = 1:length(action_scores)
    for j = 1:length(grasp_scores)
        if j ~= i
            score_total = action_scores(i) + grasp_scores(i);
            
            action_sc = abs(ranked_action_params(i,1:length(action_scale)) - action_scale);            
            for k = 1:length(task_func_action)
                if task_func_action(k) == 40
                    action_sc(action_idx(k)) = (action_sc(action_idx(k))^2)*task_func_action(k);
                else
                    action_sc(action_idx(k)) = action_sc(action_idx(k))*task_func_action(k);
                end
            end           
            action_sc = sum(action_sc);         
            
            grasp_sc = abs(ranked_grasp_params(j,1:length(grasp_scale)) - grasp_scale);
            for k = 1:length(task_func_grasp)
                if task_func_grasp(k) == 40
                    grasp_sc(grasp_idx(k)) = (grasp_sc(grasp_idx(k))^2)*task_func_grasp(k);
                else
                    grasp_sc(grasp_idx(k)) = grasp_sc(grasp_idx(k))*task_func_grasp(k);
                end
            end            
            grasp_sc = sum(grasp_sc);
            
            score_total = wt_score*score_total + wt_action*action_sc + wt_grasp*grasp_sc;
            
            if score_total < score_opt
                score_opt = score_total;
                action_part_idx = i;
                grasp_part_idx = j;
            end
        end
    end
end

action_part = action_part_idx;
grasp_part = grasp_part_idx;

end
