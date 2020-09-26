import csv
import itertools
import random

# Read csv file and save into four different dicts indexed by serial number
# Create an Actions list 
# Specify DS size desired, max being nP2 where n = number of DS points
# Create different possible nPm permutations of features, each with one of the actions
# Save to a new DS

# object1 on object2 relations
# revolute joint on 1 - grasp - yes
# pointed on 1 - type anything except wood or glass on 2 - pierce - yes

actions = ['pierce', 'grasp']
effects = ['pierced', 'grasped']
csv_file = 'obj_combo_DS.csv'

csv_file_output = 'obj_combo_labeled.csv'
csv_file_clean = 'obj_BNT.csv'
csv_pos = 'one_cls_pos.csv'
csv_neg = 'one_cls_neg.csv'
csv_bal = 'csv_balanced_pierce_grasp_no_effect.csv'

pos_dict = {'material_1':[], 'contact_1':[], 'joint_1':[], 'material_2':[], 'action':[], 'effect':[]}
neg_dict = {'material_1':[], 'contact_1':[], 'joint_1':[], 'material_2':[], 'action':[], 'effect':[]}

one_action = 'pierce'

features = {}
N_datapoints = 50000

with open(csv_file) as csvfile:
	reader = csv.reader(csvfile)
	for idx, row in enumerate(reader):
		features[idx] = row[0:4]

perm_list = range(0,len(features.keys()))
perm_list = itertools.permutations(perm_list, 2)

perm_list = [item for item in perm_list]
random.shuffle(perm_list)

if N_datapoints >= len(perm_list):
	data_points = perm_list
else:
	data_points = perm_list[0:N_datapoints+1]

output_dict = {'object1':[], 'object2':[], 'action':[], 'effect':[]}

class_nums = {'Plastic':0, 'Wood':1, 'Glass/Ceramic':2, 'Metal':3, 'Foam':4, 'flat':0, 'line':1, 'point':2, 'Fixed':0, 'Revolute':1,
				 'pierce':0, 'grasp':1, 'pierced':0, 'grasped':1, 'None':2}

one_class_nums = {'pierced':1, 'grasped':1, 'None':0}
dict_classes = {'material_1':[], 'contact_1':[], 'joint_1':[], 'material_2':[], 'action':[], 'effect':[]}

for item in data_points:
	action_num = random.randint(0,len(actions)-1)
	object1 = features[item[0]]
	object2 = features[item[1]]
	#action = one_action
	action = actions[action_num]
	effect = 'None'

	if action == 'pierce':
		if (object1[1] == 'point' or object1[2] == 'Point') and (object1[3] == 'Metal' or object1[3] == 'Wood' or object1[3] == 'Plastic'):
			if object2[3] == 'Foam':
				effect = effects[0] 
		#elif (object1[1] == 'point' or object1[2] == 'Point') and object1[3] == 'Plastic':
		#	if object2[3] == 'Foam':
		#		effect = effects[0]
	elif action == 'grasp':
		if object1[2] == 'revolute' or object1[2] == 'Revolute':
			effect = effects[1]

	if effect == 'None':
		continue

	output_dict['object1'].append(features[item[0]])
	output_dict['object2'].append(features[item[1]])
	output_dict['action'].append(action)
	output_dict['effect'].append(effect)

	material_1_class = class_nums[(features[item[0]][3]).strip()]
	contact_1_class = class_nums[(features[item[0]][1]).strip()]
	joint_1_class = class_nums[(features[item[0]][2]).strip()]
	material_2_class = class_nums[(features[item[1]][3]).strip()]
	action_class = class_nums[action]
	
	#effect_class = one_class_nums[effect]
	effect_class = class_nums[effect]
 
	dict_classes['material_1'].append(material_1_class)
	dict_classes['contact_1'].append(contact_1_class)
	dict_classes['joint_1'].append(joint_1_class)
	dict_classes['material_2'].append(material_2_class)
	dict_classes['action'].append(action_class)
	dict_classes['effect'].append(effect_class)

	if action_class == 1:
		neg_dict['material_1'].append(material_1_class)
		neg_dict['contact_1'].append(contact_1_class)
		neg_dict['joint_1'].append(joint_1_class)
		neg_dict['material_2'].append(material_2_class)
		neg_dict['action'].append(action_class)
		neg_dict['effect'].append(effect_class)
	else:
		pos_dict['material_1'].append(material_1_class)
		pos_dict['contact_1'].append(contact_1_class)
		pos_dict['joint_1'].append(joint_1_class)
		pos_dict['material_2'].append(material_2_class)
		pos_dict['action'].append(action_class)
		pos_dict['effect'].append(effect_class)

'''with open(csv_file_output, 'wb') as csv_out:
	writer = csv.writer(csv_out)
	writer.writerow(output_dict.keys())
	writer.writerows(zip(*output_dict.values()))'''

# Write it in a BNT easy form
# {material 1, contact 1, Joint 1, material 2, action, effect}

'''with open(csv_file_clean, 'wb') as csv_out:
	writer = csv.writer(csv_out)
	writer.writerow(dict_classes.keys())
	writer.writerows(zip(*dict_classes.values()))'''

rand_elts = random.sample(range(0,len(neg_dict['material_1'])+1), len(pos_dict['material_1']))

neg_dict_final = {'material_1':[], 'contact_1':[], 'joint_1':[], 'material_2':[], 'action':[], 'effect':[]}

for elt in rand_elts:
	for keys in neg_dict.keys():
		neg_dict_final[keys].append(neg_dict[keys][elt])

'''with open(csv_neg, 'wb') as csv_out:
	writer = csv.writer(csv_out)
	writer.writerow(neg_dict_final.keys())
	writer.writerows(zip(*neg_dict_final.values()))

with open(csv_pos, 'wb') as csv_out:
	writer = csv.writer(csv_out)
	writer.writerow(pos_dict.keys())
	writer.writerows(zip(*pos_dict.values()))'''

with open(csv_bal, 'wb') as csv_out:
	writer = csv.writer(csv_out)
	writer.writerow(pos_dict.keys())
	writer.writerows(zip(*pos_dict.values()))
	writer.writerows(zip(*neg_dict_final.values()))