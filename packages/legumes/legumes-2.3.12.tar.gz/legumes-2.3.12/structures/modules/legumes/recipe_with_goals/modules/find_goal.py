




'''
	find_goal (
		ingredient_names = [ 
			"protein" 
		],
		goals_ingredients = [{
			"labels": [
			  "Vitamin E"
			],
			"goal": {
				"mass + mass equivalents": {
					"per day": {
						"grams": {
							"fraction string": "3/200"
						}
					}
				}
			}
		}]
	)
'''
import rich

from fractions import Fraction
import copy

import ships.modules.exceptions.parse as parse_exception
import legumes.goals.human.FDA as human_FDA_goal
import apoplast.shows.ingredient_scan_recipe.formulate as formulate_recipe
import apoplast.measures.number.decimal.reduce as reduce_decimal
import apoplast.shows.ingredient_scan.DB.scan.seek as seek_nutrient

#
#	ingredient = "ThiamIn"
#
def find_goal_ingredient (ingredient):
	def for_each (essential):
		try:
			for name in essential ["names"]:
				if (name.lower () == ingredient.lower ()):
					return True;
					
		except Exception:
			pass;
			
		return False

	nutrient = seek_nutrient.presently (
		for_each = for_each
	)
	
	return nutrient;

'''
	using: apoplast ingredients database
	
	find where:
		goal ingredient region == composition ingredient region
'''
def find_goal (
	ingredient_names = [],
	goals_ingredients = [],
	
	records = 0
):
	#print ("find goal", ingredient_names)

	for ingredient_name in ingredient_names:
		ingredient_name_lower = ingredient_name.lower ()
		
		#print ("	ingredient:", ingredient_name_lower)
		
		try:
			composition_DB_entry_region = find_goal_ingredient (ingredient_name_lower) ["region"]
		except Exception:
			if (records >= 1):
				print ("region not found", ingredient_name_lower)
				
			continue;
		
	
		for goal in goals_ingredients:
			#print ("	goal:", goal ["labels"])
		
			for goal_label in goal ["labels"]:
				goal_label = goal_label.lower ()
				#print ("	goal_label:", goal_label)
			
				try:
					goal_DB_entry_region = find_goal_ingredient (goal_label) ["region"]
				except Exception:
					if (records >= 1):
						print ("		goal region not found")
						
					pass;
			
				if (
					composition_DB_entry_region ==
					goal_DB_entry_region
				):
					return goal;
			
				
	return None