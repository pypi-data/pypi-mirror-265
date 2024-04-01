


'''
	import legumes.recipe_with_goals.formulate as formulate_recipe_with_goals
	formulate_recipe_with_goals.beautifully (
		ingredients = [
			[ retrieve_supp ("coated tablets/multivitamin_276336.JSON"), 10 ]
		],
		goals = {}
	)
'''

'''
	fake data: {
		"info": {
			"includes": [],
			"names": [
				"protein"
			],
			"region": 1
		},
		"measures": {
			"mass + mass equivalents": {
				"per recipe": {
					"grams": {
						"fraction string": "65193545255861875341/11258999068426240"
					}
				},
				"portion of grove": {
					"fraction string": "1303870905117237506820000/3661863958435401439007099"
				}
			}
		},
		"goals": {
			"per day"
				"mass + mass equivalents": {
					"per recipe": {
							"grams": {
								"fraction string": "3/100000"
							}
					}
				}
			}
		}
	}
'''

'''
	{
		"labels": [ "Biotin" ],
		"goal": {
			"mass + mass equivalents": {
				"per day": {
					"grams": {
						"fraction string": "3/100000"
					}
				}
			}
		}
	}
'''

'''
	days = amount in recipe / amount of goal
'''

import ships.modules.exceptions.parse as parse_exception
import legumes.goals.human.FDA as human_FDA_goal
import apoplast.shows.ingredient_scan_recipe.formulate as formulate_recipe
import apoplast.measures.number.decimal.reduce as reduce_decimal
import apoplast.shows.ingredient_scan.DB.scan.seek as seek_nutrient

from .modules.find_goal import find_goal

import rich
from fractions import Fraction
import copy

def add_goals (
	essential_nutrients_grove,
	goals_ingredients,
	
	records = 0
):
	skipped_goal = []
	skipped_composition = []
	for ingredient in essential_nutrients_grove:
		assert ("info" in ingredient), ingredient
		assert ("names" in ingredient ["info"]), ingredient
	
		ingredient_names = ingredient ["info"] ["names"]
		ingredient ["goals"] = {}
		
		goal = None;
		try:
			goal = find_goal (
				ingredient_names = ingredient_names,
				goals_ingredients = goals_ingredients
			)
		except Exception as E:	
			if (records >= 1): print (parse_exception.now (E))
			skipped_goal.append (ingredient_names)
			continue;
		
		
		#rich.print_json (data = goal)
		
		#
		#	grams:
		#	
		try:
			if ("mass + mass equivalents" in ingredient ["measures"]):			
				grams_per_recipe = (
					ingredient ["measures"] ["mass + mass equivalents"] ["per recipe"] ["grams"] ["fraction string"]
				)
				grams_per_goal = (
					goal ["goal"] ["mass + mass equivalents"] ["per Earth day"] ["grams"] ["fraction string"]
				)
				goal_per_day = (
					Fraction (grams_per_recipe) / 
					Fraction (grams_per_goal)
				)
				
				decimal_string = "?"
				try:
					decimal_string = str (reduce_decimal.start (goal_per_day, partial_size = 3));
				except Exception:
					pass;
				
				ingredient ["goals"] = {
					"days of ingredient": {
						"mass + mass equivalents": {
							"per recipe": {
								"fraction string": str (goal_per_day),
								"decimal string": decimal_string
							}
						}
					}
				}
			
	
			
		except Exception as E:
			if (records >= 1): print (parse_exception.now (E))
			skipped_composition.append (ingredient_names)
			pass;
			
		
		if ("unites" in ingredient):
			#raise Exception ("unites")
		
			add_goals (
				ingredient ["unites"],
				goals_ingredients
			)

	return [
		skipped_goal,
		skipped_composition
	]

def beautifully (
	recipe = None,
	ingredients = [],
	goals = {},
	
	records = 0
):
	if (type (recipe) != dict):
		recipe = formulate_recipe.adroitly (
			ingredients
		)
		
	essential_nutrients = recipe ["essential nutrients"]
	essential_nutrients_grove = essential_nutrients ["grove"]
	cautionary_ingredients = recipe ["cautionary ingredients"]
	
	if (
		type (goals) != dict or 
		(type (goals) == dict and "ingredients" not in goals)
	):
		return {
			"recipe": recipe,
			"skipped_composition": [],
			"skipped_goal": [],
			"note": "goal ingredients not found"
		};
		
	
	recipe ["goals"] = goals	
	goals_ingredients = goals ["ingredients"];
	
	[ skipped_goal, skipped_composition ] = add_goals (
		essential_nutrients_grove,
		goals_ingredients
	)
	

	return {
		"recipe": recipe,
		"skipped_composition": skipped_composition,
		"skipped_goal": skipped_goal
	};
	
	
