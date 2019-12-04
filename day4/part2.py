#!/usr/bin/env python

# import re
# import math
# import collections

# guessed wrong: 657

DEFAULT_RANGE = "234208,765869"

def check(n):
	found_two = False
	repeat_count = 1
	last = None
	for c in str(n):
		if last and last == c:
			repeat_count += 1
		elif repeat_count == 2:
			found_two = True
			repeat_count = 1
		else:
			repeat_count = 1
		if last and c < last:
			return False
		last = c
	return found_two or repeat_count == 2


def main(args):
	if args.test:
		x = check(args.test)
		print("Test of {} = {}".format(args.test, x))
		exit(0)
	matches = 0
	(start,end) = map(int, args.range.split(','))
	for x in range(start,end+1):
		if check(x):
			matches += 1
	print("There are {} matches".format(matches))

if __name__ == '__main__':
	import argparse

	parser = argparse.ArgumentParser()
	parser.add_argument('-r', '--range', help='Range, like "123,456"', default=DEFAULT_RANGE)
	parser.add_argument('-t', '--test', type=int)
	args = parser.parse_args()

	main(args)
