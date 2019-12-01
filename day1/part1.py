#!/usr/bin/env python

from math import floor

DEFAULT_INPUT_FILE = "input/part1.txt"

def main(args):
	with open(args.file, "r") as fh:
		total = 0
		for line in fh:
			if line.strip() == '':
				pass
			x = int(line.strip())
			total += floor(x/3) - 2
	print(int(total))

if __name__ == '__main__':
	import argparse

	parser = argparse.ArgumentParser()
	parser.add_argument('-f', '--file', help='Input file, default: {}'.format(DEFAULT_INPUT_FILE), default=DEFAULT_INPUT_FILE)
	args = parser.parse_args()

	main(args)
