#!/usr/bin/env python

import re
# import math
# import collections
from copy import copy
from itertools import permutations

# Wrong answer: 41583


DEFAULT_INPUT_FILE = "input/part1.txt"

class Stack(object):
	def __init__(self, l=None):
		self.l = l or []

	def __repr__(self):
		return str(self.l)

	def pop(self):
		return self.l.pop(0)

	def push(self, v):
		self.l.insert(0, v)

def get_param_value(codes, param_value, mode):
	if mode == '0':
		print("Returning value from codes[{}] -> {}".format(param_value, codes[param_value]))
		return codes[param_value]
	elif mode == '1':
		return param_value
	else:
		print("unexpected mode passed to get_param_value: param_value = {}, mode = {}".format(param_value, mode))
		exit(1)

def debug_instruction(l):
	print("""
operator_string: {}
code: {}
modes: {}
params: {}
------------
""".format(*l))


def perform_calculation(codes, io=None, index=0, debug=False):
	operator_string = "{:05d}".format(codes[index])
	code = int(operator_string[-2:])
	modes = operator_string[:3]
	if io is None:
		io = Stack()

	if code == 99:
		return io

	get_params = lambda n: [codes[index+i] for i in range(1,n+1)]
	param_count = 0
	instruction_pointer = None

	if code == 1:
		# -- ADDITION
		param_count = 3
		params = get_params(param_count)
		if debug:
			debug_instruction([operator_string, code, modes, params])
		a = get_param_value(codes, params[0], modes[2])
		b = get_param_value(codes, params[1], modes[1])
		codes[params[2]] = a + b
	elif code == 2:
		# -- MULTIPLICATION
		param_count = 3
		params = get_params(param_count)
		if debug:
			debug_instruction([operator_string, code, modes, params])
		a = get_param_value(codes, params[0], modes[2])
		b = get_param_value(codes, params[1], modes[1])
		print("a: {}, b: {}".format(a, b))
		codes[params[2]] = a * b
	elif code == 3:
		# INPUT COPY
		param_count = 1
		params = get_params(param_count)
		if debug:
			debug_instruction([operator_string, code, modes, params])
		codes[params[0]] = io.pop()
	elif code == 4:
		# OUTPUT
		param_count = 1
		params = get_params(param_count)
		if debug:
			debug_instruction([operator_string, code, modes, params])
		a = get_param_value(codes, params[0], modes[2])
		io.push(a)
	elif code == 5:
		# JUMP IF TRUE
		param_count = 2
		params = get_params(param_count)
		if debug:
			debug_instruction([operator_string, code, modes, params])
		a = get_param_value(codes, params[0], modes[2])
		b = get_param_value(codes, params[1], modes[1])
		if a:
			instruction_pointer = b
	elif code == 6:
		# JUMP IF FALSE
		param_count = 2
		params = get_params(param_count)
		if debug:
			debug_instruction([operator_string, code, modes, params])
		a = get_param_value(codes, params[0], modes[2])
		b = get_param_value(codes, params[1], modes[1])
		if not a:
			instruction_pointer = b
	elif code == 7:
		# LESS THAN
		param_count = 3
		params = get_params(param_count)
		if debug:
			debug_instruction([operator_string, code, modes, params])
		a = get_param_value(codes, params[0], modes[2])
		b = get_param_value(codes, params[1], modes[1])
		codes[params[2]] = 1 if a < b else 0
		pass
	elif code == 8:
		# EQUALS
		param_count = 3
		params = get_params(param_count)
		if debug:
			debug_instruction([operator_string, code, modes, params])
		a = get_param_value(codes, params[0], modes[2])
		b = get_param_value(codes, params[1], modes[1])
		codes[params[2]] = 1 if a == b else 0

	next_index = instruction_pointer if instruction_pointer is not None else index + 1 + param_count
	perform_calculation(codes, io, index=next_index)


def run_pipeline(instructions, order, starting_input=0, debug=False):
	io = Stack([starting_input])
	for i in range(5):
		io.push(order[i])
		x = copy(instructions)
		print("Starting calculations with this input: {}".format(io))
		perform_calculation(x, io, debug=debug)
	return io.pop()


def main(args):
	with open(args.file, "r") as fh:
		for line in fh:
			if line.strip() == '':
				pass
			x = map(int, line.split(','))

	all_perms = list(permutations([0,1,2,3,4]))
	max_result = None
	for p in all_perms:
		out = run_pipeline(x, p, debug=args.debug)
		if max_result is None or out > max_result:
			max_result = out

	print("Max output is {}".format(max_result))


if __name__ == '__main__':
	import argparse

	parser = argparse.ArgumentParser()
	parser.add_argument('-f', '--file', help='Input file, default: {}'.format(DEFAULT_INPUT_FILE), default=DEFAULT_INPUT_FILE)
	parser.add_argument('-d', '--debug', default=False, action="store_true", help="Debug info")
	args = parser.parse_args()

	main(args)
