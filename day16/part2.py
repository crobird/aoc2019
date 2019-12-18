#!/usr/bin/env python

# import re
from math import floor, ceil
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
	inputs_len = len(inputs)
	dprint(debug, "Length of inputs: {}".format(inputs_len))
	for phase_index in xrange(phase_count):
		dprint(debug, "PHASE {} inputs: {}".format(phase_index, int_list_as_str(inputs)))
		next_inputs = []

		# Handle the first half - floor(n/2)
		input_index = 0
		while input_index < floor(inputs_len/2):
			total = 0
			pattern_length = 4 * (input_index + 1)
			neg_skew = 2 * (input_index + 1)
			dprint(debug, "-- input_index: {} -- pattern_length={}, neg_skew={}".format(input_index, pattern_length, neg_skew))

			for input_index2 in xrange(inputs_len):
				pos_start = (input_index2 - input_index) % pattern_length
				neg_start = (input_index2 - input_index - neg_skew) % pattern_length
				dprint(debug, "pos_start={}, neg_start={}".format(pos_start, neg_start))
				if pos_start >= 0 and pos_start < (input_index + 1):
					dprint(debug, "1 at {}".format(input_index2))
					total += inputs[input_index2]
				elif neg_start >= 0 and neg_start < (input_index + 1):
					dprint(debug, "N at {}".format(input_index2))
					total -= inputs[input_index2]

			dprint(debug, "ADDING {}".format(str(total)[-1]))
			next_inputs.append(int(str(total)[-1]))
			input_index += 1

		next_inputs2 = []
		total = 0
		for input_index in xrange(inputs_len, int(floor(inputs_len/2)), -1):
			dprint(debug, "-- input_index: {} -- Adding inputs[{}]".format(input_index, input_index-1))
			total += inputs[input_index-1]
			next_inputs2.insert(0, int(str(total)[-1]))			


		next_inputs.extend(next_inputs2)	
		dprint(debug, "OUTPUT: {}".format(int_list_as_str(next_inputs, join_char="")))
		inputs = next_inputs
	return next_inputs


def OLD_run_phases(first_inputs, phase_count, debug=False):
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
			inputs = [int(x) for x in line.strip()]*10000

	output = run_phases(inputs, args.n_phases, args.debug)
	output_offset = int(int_list_as_str(inputs[:7], join_char=""))
	short_output = output[output_offset:output_offset+8]
	print("First 8 chars of output after {} phases is {}".format(args.n_phases, int_list_as_str(short_output, join_char="")))

if __name__ == '__main__':
	import argparse

	parser = argparse.ArgumentParser()
	parser.add_argument('-f', '--file', help='Input file, default: {}'.format(DEFAULT_INPUT_FILE), default=DEFAULT_INPUT_FILE)
	parser.add_argument('-n', '--n_phases', type=int, help="Number of phases to run", default=5)
	parser.add_argument('-d', '--debug', default=False, action="store_true", help="See some cool debug stuff")
	args = parser.parse_args()

	main(args)
