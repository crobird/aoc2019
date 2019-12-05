#!/usr/bin/env python

import re
# import math
# import collections
from copy import copy


DEFAULT_INPUT_FILE = "input/part1.txt"

def get_param_value(codes, param_value, mode):
	if mode == '0':
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


def perform_calculation(codes, input_value, index=0):
	operator_string = "{:05d}".format(codes[index])
	code = int(operator_string[-2:])
	modes = operator_string[:3]

	if code == 99:
		return

	get_params = lambda n: [codes[index+i] for i in range(1,n+1)]
	param_count = 0

	if code == 1:
		param_count = 3
		params = get_params(param_count)
		# debug_instruction([operator_string, code, modes, params])
		a = get_param_value(codes, params[0], modes[2])
		b = get_param_value(codes, params[1], modes[1])
		codes[params[2]] = a + b
	elif code == 2:
		param_count = 3
		params = get_params(param_count)
		# debug_instruction([operator_string, code, modes, params])
		a = get_param_value(codes, params[0], modes[2])
		b = get_param_value(codes, params[1], modes[1])
		codes[params[2]] = a * b
	elif code == 3:
		param_count = 1
		params = get_params(param_count)
		# debug_instruction([operator_string, code, modes, params])
		codes[params[0]] = input_value
	elif code == 4:
		param_count = 1
		params = get_params(param_count)
		# debug_instruction([operator_string, code, modes, params])
		a = get_param_value(codes, params[0], modes[2])
		print("OUTPUT FOR param {} with mode {} is {}".format(params[0], modes[2], a))

	perform_calculation(codes, input_value, index=(index + 1 + param_count))


def main(args):
	with open(args.file, "r") as fh:
		for line in fh:
			if line.strip() == '':
				pass
			x = map(int, line.split(','))

	perform_calculation(x, 1)

if __name__ == '__main__':
	import argparse

	parser = argparse.ArgumentParser()
	parser.add_argument('-f', '--file', help='Input file, default: {}'.format(DEFAULT_INPUT_FILE), default=DEFAULT_INPUT_FILE)
	args = parser.parse_args()

	main(args)
