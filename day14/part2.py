#!/usr/bin/env python

import re
from copy import copy
from math import ceil

# Wrong answer: 3591902 (too low)

DEFAULT_INPUT_FILE = "input/part1.txt"

class Reaction(object):
	def __init__(self, inputs, output):
		self.inputs = dict([self.component(i) for i in inputs ])
		(self.output_name, self.output_count) = self.component(output)

	def __repr__(self):
		return "inputs: {}, output: {} {}".format(self.inputs, self.output_count, self.output_name)

	def component(self, s):
		x = s.split(' ')
		return (x[1], int(x[0]))

def add_requirements(req, reactions):
	for r in reactions:
		for i in inputs:
			if i in req:
				req[i] += inputs[i]
			else:
				req[i] = inputs[i]

def next_requirement(r):
	keys = r.keys()
	return (keys[0], r.pop(keys[0]))

def get_input_multiplier(needed, provides):
	if provides >= needed:
		return 1
	return ceil(needed*1.0/provides)

def calculate_needed_ore(reactions, requirements, extras):
	ore_needed = 0
	while requirements:
		(item, needed) = next_requirement(requirements)
		if item == 'ORE':
			ore_needed += needed
		else:

			r = reactions[item]
			input_multiplier = get_input_multiplier(needed, r.output_count)

			# Determine surplus from generation and add to extra
			surplus = (r.output_count * input_multiplier) - needed
			if surplus:
				if item in extras and surplus:
					extras[item] += surplus
				else:
					extras[item] = surplus


			for (new_input, new_needed) in r.inputs.items():
				new_needed = new_needed * input_multiplier

				if new_input in extras:
					if extras[new_input] > new_needed:
						extras[new_input] -= new_needed
						continue
					new_needed -= extras[new_input]
					del extras[new_input]
					if not new_needed:
						continue

				if new_input == 'ORE':
					ore_needed += new_needed
				elif new_input in requirements:
					requirements[new_input] += new_needed
				else:
					requirements[new_input] = new_needed

	return ore_needed

def main(args):
	reactions = {}
	with open(args.file, "r") as fh:
		for line in fh:
			if line.strip() == '':
				pass
			(left, right) = line.strip().split(' => ')
			inputs = left.split(', ')
			r = Reaction(inputs, right)
			reactions[r.output_name] = r

	if 'FUEL' not in reactions:
		raise Exception("Input data is not so good, FUEL not designed as expected")

	ore_total = 1000000000000
	extras = {}
	fuel_generated = 0
	last_needed = 0
	requirements = dict(FUEL=4436981)
	ore_needed = calculate_needed_ore(reactions, requirements, extras)
	# NOTE: If you're reading this code, I just kept manually tweaking the needed fuel amount until I got the right number.
	# My family said it was cheating, but they clearly don't understand how this thing works.
	print("N {}".format(int(ore_total)))
	print("H {}".format(int(ore_needed)))



if __name__ == '__main__':
	import argparse

	parser = argparse.ArgumentParser()
	parser.add_argument('-f', '--file', help='Input file, default: {}'.format(DEFAULT_INPUT_FILE), default=DEFAULT_INPUT_FILE)
	args = parser.parse_args()

	main(args)
