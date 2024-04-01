








'''
	python3 status.proc.py recipe_with_goals/_status/0_1_basics/status_1.py
'''


import apoplast.clouds.food_USDA.deliveries.one.assertions.foundational as assertions_foundational
import apoplast.clouds.food_USDA.examples as USDA_examples	
import apoplast.clouds.food_USDA.nature as food_USDA_nature
import apoplast.insure.equality as equality

import apoplast.shows.ingredient_scan_recipe.formulate as formulate_recipe
import apoplast.shows.ingredient_scan.grove.seek_name_or_accepts as grove_seek_name_or_accepts

import apoplast.clouds.supp_NIH.nature as supp_NIH_nature
import apoplast.clouds.supp_NIH.examples as NIH_examples

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
		[ retrieve_supp ("coated tablets/multivitamin_276336.JSON"), 10 ]
	])
	
	add ("status_1.JSON", json.dumps (recipe, indent = 4))
	
	assert (len (recipe ["essential nutrients"] ["natures"]) == 1)

	rich.print_json (data = recipe)
	
checks = {
	"check 1": check_1
}