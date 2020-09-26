%% Returns updated domain and problem definitions that incorporate the new object actions and effects

% Input: Original domain and problem definitions, tool output by Abelha
% code, desired effect input into MGP module and the level of Macgyvering
% Output: 

function [] = plan_augment(domain_in, problem_in, tool, action, effect)

domain_ID = fopen(domain_in);
domain_out = fopen('MGP_domain.pddl','w');

problem_ID = fopen(problem_in);
problem_out = fopen('MGP_problem.pddl','w');

input_file = tool;

% Generate a tool ID
randID = randi(10,1);
tool_name = string(strtok(input_file,'_'))+string(randID);

%% Write updated domain definition

type_def = sprintf("\t(:types %s - object)\n", string(randID)); 

% Add :type to domain file
tline = fgetl(domain_ID)
fprintf(domain_out, string(tline));
fprintf(domain_out, "\n");
while ischar(tline)
    % Add type if action unknown
    if contains(tline,'requirements') && action ~= ""
        fprintf(domain_out, type_def);
        fprintf(domain_out, "\n");
    end
    
    if contains(tline,string(action)) %--> In action line, next line is parameters
        fprintf(domain_out, string(tline));
        fprintf(domain_out, "\n");
        tline = fgetl(domain_ID) %--> parameters line
        C = strsplit(tline)
        desired_type = C{4} % Assuming the 4th parameter will be desired type
        fprintf(domain_out, tline);
        fprintf(domain_out, "\n");
    end
    
    tline = fgetl(domain_ID)
    if ischar(tline)
        fprintf(domain_out, string(tline));
        fprintf(domain_out, "\n");
    end
    
end

% Action definition for tools in domain - NEED TO MOVE IT BEFORE FINAL )
switch action
    % Level 2 and 3 MacGyvering - unknown action
    case ""
        action_def = sprintf("\t (:action %s \n", effect); 
        param_def = sprintf("\t \t :parameters (?with - %s ?on) \n", string(randID));
        precon_def = "\t \t :precondition (have ?with) \n";
        effect_def = sprintf("\t \t :effect (%s ?on) \n", string(effect));
    
        fprintf(domain_out, action_def);
        fprintf(domain_out, param_def);
        fprintf(domain_out, precon_def);
        fprintf(domain_out, effect_def);  
        fprintf(domain_out, "\t ) \n");
    otherwise 
        % Unknown action does not follow above template
        % Or need to write code that automatically finds desired affordance
end

%% Write updated problem definition

% Add :objects to problem definition
tline = fgetl(problem_ID);
fprintf(problem_out, string(tline));
fprintf(problem_out, "\n");
while ischar(tline)
    if contains(tline,'domain')
        tline = fgetl(problem_ID); %--> points to :objects if it exists
        if contains(tline,'objects')
            C = strsplit(tline);
            C_new = strjoin([string(C{2}),sprintf(" %s - %s ", tool_name, desired_type)]);
            C{2} = C_new;
            fprintf(problem_out, strjoin([C{2:size(C,2)}]));
            fprintf(problem_out, "\n");
        else
            initial_def = sprintf("\t (:objects %s - %s)\n", tool_name, randID);
            fprintf(problem_out, initial_def);
        end
        %tline = fgetl(problem_ID);
        %continue
    end
    tline = fgetl(problem_ID);
    if ischar(tline)
        fprintf(problem_out, string(tline));
        fprintf(problem_out, "\n");
    end
end

fclose('all');
end




