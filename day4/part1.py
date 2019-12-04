#!/usr/bin/env python

# import re
# import math
# import collections


DEFAULT_RANGE = "234208,765869"

def check(n):
	found_repeat = False
	last = None
	for c in str(n):
		if not found_repeat and last and last == c:
			found_repeat = True
		if last and c < last:
			return False
		last = c
	return found_repeat


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
