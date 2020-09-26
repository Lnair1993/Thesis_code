# Arbitrating between tool substitution and tool construction
from pierce_predict.py import *

def add_substitutes(objects_attr, object_rank, objects_list):
	# Add the single objects to object_rank, with geoscore from pierce predict, material of zero, att type of 'subs' and att score of 0.
	idx = len(object_rank)

	for obj in objects_list:
		object_rank.append(((obj), idx))
		objects_attr[((obj), idx)] = {'geoscore':0, 'att_type':'subs', 'att_score':0, 'material_score':0, 'total_score':0}
		idx = idx + 1

	return objects_attr, object_rank 

def rule_based():
	# Set fixed geoscore, att score to 0, material of 0 and att type of 'subs'
	return None

def normalization(objects_attr, ):
	# Set geoscore from pierce predict for substitutes, geoscore predict for constructions, material of 0, att type of 'subs' or actual type, att score of 0 or actual

	return None

def dual_score():
	# Set geoscore from piece predict for substitutes, material of 0, att type of 'subs' or actual type, att score of 0 or actual 
	return None