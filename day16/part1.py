#!/usr/bin/env python

# import re
# import math
# import collections


DEFAULT_INPUT_FILE = "input/part1.txt"

def dprint(debug, s):
	if debug:
		print(s)

def get_pattern(n):
	default = [0, 1, 0, -1]
	pattern = []
	for i in default:
		pattern.extend([i]*(n+1))
	return pattern

def int_list_as_str(l, join_char=","):
	return join_char.join(map(str, l))

def run_phases(first_inputs, phase_count, debug=False):
	inputs = first_inputs
	for n in range(phase_count):
		dprint(debug, "PHASE {} inputs: {}".format(n, int_list_as_str(inputs)))
		next_inputs = []
		for input_index in range(len(inputs)):
			pattern_index = 1
			pattern = get_pattern(input_index)
			dprint(debug, "Pattern for index {} is {}".format(input_index, int_list_as_str(pattern)))
			total = 0
			for input_index2 in range(len(inputs)):
				output = []
				total += inputs[input_index2] * pattern[pattern_index]
				pattern_index = (pattern_index + 1) % len(pattern)
			next_inputs.append(int(str(total)[-1]))
		inputs = next_inputs
	return next_inputs

def main(args):
	inputs = None
	with open(args.file, "r") as fh:
		for line in fh:
			if line.strip() == '':
				pass
			if inputs:
				raise Exception("Saw more than one line of inputs. Whaaaa?")
			inputs = [int(x) for x in line.strip()]

	output = run_phases(inputs, args.n_phases, args.debug)
	print("First 8 chars of output after {} phases is {}".format(args.n_phases, int_list_as_str(output[:8], join_char="")))

if __name__ == '__main__':
	import argparse

	parser = argparse.ArgumentParser()
	parser.add_argument('-f', '--file', help='Input file, default: {}'.format(DEFAULT_INPUT_FILE), default=DEFAULT_INPUT_FILE)
	parser.add_argument('-n', '--n_phases', type=int, help="Number of phases to run", default=5)
	parser.add_argument('-d', '--debug', default=False, action="store_true", help="See some cool debug stuff")
	args = parser.parse_args()

	main(args)
