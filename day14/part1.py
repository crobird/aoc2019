#!/usr/bin/env python

import re
from copy import copy
from math import ceil

# Wrong answer: 233638 (too low)

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

	requirements = copy(reactions['FUEL'].inputs)
	extras = {}
	ore_needed = 0
	while requirements:
		print("requirements before: {}".format(requirements))
		(item, needed) = next_requirement(requirements)
		if item == 'ORE':
			ore_needed += needed
		else:
			print("looking for {} {}".format(needed, item))

			r = reactions[item]
			input_multiplier = get_input_multiplier(needed, r.output_count)

			# Determine surplus from generation and add to extra
			surplus = (r.output_count * input_multiplier) - needed
			if surplus:
				print("Will generate {} in increments of {}, so we need to generate {}, leftover = {}".format(item, r.output_count, (r.output_count * input_multiplier), surplus))
				if item in extras and surplus:
					extras[item] += surplus
				else:
					extras[item] = surplus


			for (new_input, new_needed) in r.inputs.items():
				print("\tGonna need {} x {} {}".format(new_needed, input_multiplier, new_input))
				new_needed = new_needed * input_multiplier

				if new_input in extras:
					print("Found some in extras!")
					if extras[new_input] > new_needed:
						extras[new_input] -= new_needed
						continue
					new_needed -= extras[new_input]
					del extras[new_input]
					if not new_needed:
						continue
					print("Now I only need {}".format(new_needed))

				if new_input == 'ORE':
					ore_needed += new_needed
				elif new_input in requirements:
					requirements[new_input] += new_needed
				else:
					requirements[new_input] = new_needed

		print("requirements after: {}".format(requirements))

	print("Ore needed = {}".format(ore_needed))


if __name__ == '__main__':
	import argparse

	parser = argparse.ArgumentParser()
	parser.add_argument('-f', '--file', help='Input file, default: {}'.format(DEFAULT_INPUT_FILE), default=DEFAULT_INPUT_FILE)
	args = parser.parse_args()

	main(args)
