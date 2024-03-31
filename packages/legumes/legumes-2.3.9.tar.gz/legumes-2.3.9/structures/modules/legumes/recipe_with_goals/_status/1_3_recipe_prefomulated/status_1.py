















'''
	python3 status.proc.py recipe_with_goals/_status/1_3_recipe_prefomulated/status_1.py
'''


#
#	foods
#
import apoplast.clouds.food_USDA.deliveries.one.assertions.foundational as assertions_foundational
import apoplast.clouds.food_USDA.examples as USDA_examples	
import apoplast.clouds.food_USDA.nature as food_USDA_nature

#
#	supps
#
import apoplast.clouds.supp_NIH.nature as supp_NIH_nature
import apoplast.clouds.supp_NIH.examples as NIH_examples
import apoplast.insure.equality as equality
import apoplast.shows.ingredient_scan_recipe.formulate as formulate_recipe
import apoplast.shows.ingredient_scan.grove.seek_name_or_accepts as grove_seek_name_or_accepts
import apoplast.shows.ingredient_scan_recipe.formulate as formulate_recipe

#
#	
#
import legumes.recipe_with_goals.formulate as formulate_recipe_with_goals
import legumes.goals.human.FDA as human_FDA_goal
	
import rich

from fractions import Fraction
from copy import deepcopy
import json

def find_grams (measures):
	return Fraction (
		measures ["mass + mass equivalents"] ["per recipe"] ["grams"] ["fraction string"]
	)
	
def add (path, data):
	import pathlib
	from os.path import dirname, join, normpath
	this_directory = pathlib.Path (__file__).parent.resolve ()
	example_path = normpath (join (this_directory, path))
	FP = open (example_path, "w")
	FP.write (data)
	FP.close ()
	
def retrieve_supp (supp_path):
	return supp_NIH_nature.create (
		NIH_examples.retrieve (supp_path) 
	)

def retrieve_food (food_path):
	return food_USDA_nature.create (
		USDA_examples.retrieve (food_path)
	)

def check_1 ():
	recipe = formulate_recipe.adroitly ([
		[ retrieve_supp ("coated tablets/multivitamin_276336.JSON"), 10 ],
		[ retrieve_supp ("other/chia_seeds_214893.JSON"), 20 ],
		[ retrieve_food ("branded/beet_juice_2412474.JSON"), 20 ],
		[ retrieve_food ("branded/beet_juice_2642759.JSON"), 20 ],
		[ retrieve_food ("branded/Gardein_f'sh_2663758.JSON"), 20 ],
		[ retrieve_food ("branded/impossible_beef_2664238.JSON"), 80 ],
	])

	recipe_with_goals = formulate_recipe_with_goals.beautifully (
		recipe = recipe,
		goals = human_FDA_goal.retrieve ()
	)
	
	add (
		"status_1.JSON", 
		json.dumps (recipe_with_goals, indent = 4)
	)
	
	
	
checks = {
	"check 1": check_1
}