





'''
	This has a simultaneous DB lookup issue perhaps...?
'''




'''
	python3 status.proc.py recipe_with_goals/_status/1_1_recipe/status_1.py
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
	
		
	
		
	'''
	recipe = formulate_recipe.adroitly ([
		[ retrieve_supp ("coated tablets/multivitamin_276336.JSON"), 10 ]
	])
	'''
		
	recipe_with_goals = formulate_recipe_with_goals.beautifully (
		ingredients = [
			[ retrieve_supp ("coated tablets/multivitamin_276336.JSON"), 10 ]
		],
		goals = human_FDA_goal.retrieve ()
	)
	
	add (
		"status_1.JSON", 
		json.dumps (recipe_with_goals, indent = 4)
	)
	
	
	'''	
		per recipe:				3/100 * 90 * 10 = 27
		per day:				3/200
		
		days of ingredient: 	(27) / (3/200) = 1800
	'''
	
	
	
	vitamin_E = grove_seek_name_or_accepts.politely (
		grove = recipe_with_goals ["recipe"] ["essential nutrients"] ["grove"],
		name_or_accepts = "vitamin e"
	)
	rich.print_json (data = vitamin_E)
	assert (
		vitamin_E ["goals"] ["days of ingredient"] ["mass + mass equivalents"] ["per recipe"] ["fraction string"] == 
		"1800"
	), vitamin_E ["goals"]
	
	
	'''
		per recipe:				.050 * 90 * 10 = 45
			per form: .050
		
		per day:				2/125
		
		days of ingredient:		45 / (2/125) = 2812.5 = 5625/2
	'''
	vitamin_B3 = grove_seek_name_or_accepts.politely (
		grove = recipe_with_goals ["recipe"] ["essential nutrients"] ["grove"],
		name_or_accepts = "vitamin b3"
	)
	rich.print_json (data = vitamin_B3)
	assert (
		vitamin_B3 ["goals"] ["days of ingredient"] ["mass + mass equivalents"] ["per recipe"] ["fraction string"] == 
		"5625/2"
	), vitamin_B3 ["goals"] ["days of ingredient"] ["mass + mass equivalents"] ["per recipe"] ["fraction string"]
	
checks = {
	"check 1": check_1
}