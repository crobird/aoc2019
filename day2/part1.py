#!/usr/bin/env python

# import re
# import math
# import collections


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

	x[1] = 12
	x[2] = 2
	perform_calculation(x)

	print("value at index 0 is {}".format(x[0]))

if __name__ == '__main__':
	import argparse

	parser = argparse.ArgumentParser()
	parser.add_argument('-f', '--file', help='Input file, default: {}'.format(DEFAULT_INPUT_FILE), default=DEFAULT_INPUT_FILE)
	args = parser.parse_args()

	main(args)
