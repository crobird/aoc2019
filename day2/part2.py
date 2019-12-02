#!/usr/bin/env python

# import re
# import math
# import collections
from copy import copy


DEFAULT_INPUT_FILE = "input/part1.txt"

def perform_calculation(codes, index=0):
	code = codes[index]
	if code == 1:
		a = codes[index+1]
		b = codes[index+2]
		c = codes[index+3]
		codes[c] = codes[a] + codes[b]
	elif code == 2:
		a = codes[index+1]
		b = codes[index+2]
		c = codes[index+3]
		codes[c] = codes[a] * codes[b]
	elif code == 99:
		return
	perform_calculation(codes, index=index+4)


def main(args):
	with open(args.file, "r") as fh:
		for line in fh:
			if line.strip() == '':
				pass
			x = map(int, line.split(','))

	for noun in range(100):
		for verb in range(100):
			y = copy(x)
			y[1] = noun
			y[2] = verb
			perform_calculation(y)
			if y[0] == 19690720:
				print("noun = {}, verb = {}, answer = {}".format(noun, verb, (100 * noun) + verb))
				break


if __name__ == '__main__':
	import argparse

	parser = argparse.ArgumentParser()
	parser.add_argument('-f', '--file', help='Input file, default: {}'.format(DEFAULT_INPUT_FILE), default=DEFAULT_INPUT_FILE)
	args = parser.parse_args()

	main(args)
