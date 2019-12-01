#!/usr/bin/env python

from math import floor

DEFAULT_INPUT_FILE = "input/part1.txt"

def get_fuel(n, total):
	fuel = floor(n/3) - 2
	if fuel <= 0:
		return total
	else:
		return get_fuel(fuel, total + fuel)

def main(args):
	with open(args.file, "r") as fh:
		total = 0
		for line in fh:
			if line.strip() == '':
				pass
			mass = int(line.strip())
			total += get_fuel(mass, 0)
			
	print(int(total))

if __name__ == '__main__':
	import argparse

	parser = argparse.ArgumentParser()
	parser.add_argument('-f', '--file', help='Input file, default: {}'.format(DEFAULT_INPUT_FILE), default=DEFAULT_INPUT_FILE)
	args = parser.parse_args()

	main(args)
