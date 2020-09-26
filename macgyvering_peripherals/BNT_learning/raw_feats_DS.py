import csv
import random
import itertools

# 1) Read the filenames in the DS - CHECK
# 2) Generate their random permutations - CHECK
# 3) For each, extract the SHOT-C features for the first object - CHECK
# 4) For each, extract material properties of both objects - CHECK
# 5) For each, extract contact type of first object - CHECK
# 6) For each, extract joint type of first object - CHECK
# 7) Replace the material properties with corresponding class
# 8) For each permutation, train a single binary classifier for each action
# 9) Use the contact type, material properties to create DS for pierce action
# 10) Use the joint type, to create DS for grasp action
# 11) Create a balanced DS combining both pierce and grasp actions 

csv_properties = 'parts_material_joint.csv'
csv_SHOTC = 'ShotC_reduced.csv'

# Output files - both balanced and unbalanced
csv_balanced = 'raw_feats_bal.csv'
csv_unbalanced = 'raw_feats_unbal.csv'

# Initialize a dict for the properties and features
shot_C = {}
object_props = {}
filenames = []

# Save final features
pos_feats = {'obj_0':[], 'material_0':[], 'material_1':[], 'effect':[]}
neg_feats = {'obj_0':[], 'material_0':[], 'material_1':[], 'effect':[]}
header = ['obj_0', 'material_0', 'material_1']
final_feats = []

single_action = True
action = 'grasp'

with open(csv_SHOTC) as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in csvfile:
        row = row.split(',')
        shot_C[row[0]] = map(float, row[1:len(row)])
        filenames.append(row[0])

with open(csv_properties) as csvfile:
    reader = csv.reader(csvfile)
    next(reader, None) # Skip the header
    for row in csvfile:
        row = row.split(',')
        object_props[row[0]] = {'material': row[1], 'joint':row[2], 'contact':row[3]}

#print object_props

class_nums = {'plastic':0, 'wood':1, 'ceramic':2, 'metal':3, 'foam':4, 'flat':0, 'line':1, 'point':2, 'fixed':0, 'revolute':1,
				 'pierce':0, 'grasp':1, 'pierced':0, 'grasped':1, 'none':2}

# Create permutation of file names
perm_list = range(0, len(filenames))
perm_list = itertools.permutations(perm_list, 2)
perm_list = [item for item in perm_list] # Make it a list of permutations

for pair in perm_list:
    obj_0 = filenames[pair[0]]
    obj_1 = filenames[pair[1]]
    effect = 0 # No effect

    if action == 'pierce':
		if ('point' in object_props[obj_0]['contact']) and ('foam' not in object_props[obj_0]['material']):
			if 'foam' in object_props[obj_1]['material']:
				effect = 1 # Pierceable
    elif action == 'grasp':
		if 'revolute' in object_props[obj_0]['joint']:
			effect = 1 # Graspable

    material_0_class = class_nums[object_props[obj_0]['material']]
    material_1_class = class_nums[object_props[obj_1]['material']]

    if effect == 0:
        neg_feats['obj_0'].append(shot_C[obj_0])
        neg_feats['material_0'].append(material_0_class)
        neg_feats['material_1'].append(material_1_class)
        neg_feats['effect'].append(effect)
    else:
        pos_feats['obj_0'].append(shot_C[obj_0])
        pos_feats['material_0'].append(material_0_class)
        pos_feats['material_1'].append(material_1_class)
        pos_feats['effect'].append(effect)

    final_feats.append([shot_C[obj_0]] + [object_props[obj_0]['material']] + [object_props[obj_1]['material']] + [effect])


with open(csv_unbalanced, 'wb') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(header)
    writer.writerows(final_feats)

# Create a balanced dataset
num_neg_elts = len(neg_feats['obj_0'])
num_pos_elts = len(pos_feats['obj_0'])
bal_feats = []
new_dict = {'obj_0':[], 'material_0':[], 'material_1':[], 'effect':[]}
pos_flag = False # Flag indicating if pos or neg dict is larger

if num_neg_elts > num_pos_elts: # Negative examples are more
    temp_list = range(0, num_neg_elts)
    random.shuffle(temp_list)
    temp_list = temp_list[0:num_pos_elts]

    for elt in temp_list:
	    for key in neg_feats.keys():
		    new_dict[key].append(neg_feats[key][elt])

    pos_flag = True

else: # Positive examples are more
    temp_list = range(0, num_pos_elts)
    random.shuffle(temp_list)
    temp_list = temp_list[0:num_neg_elts]

    for elt in temp_list:
	    for key in pos_feats.keys():
		    new_dict[key].append(pos_feats[key][elt])
    
    pos_flag = False

with open(csv_balanced, 'wb') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(new_dict.keys())
    writer.writerows(zip(*new_dict.values()))

    if pos_flag: # Positive examples retained
        writer.writerows(zip(*pos_feats.values()))
    else:
        writer.writerows(zip(*neg_feats.values()))








