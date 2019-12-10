#!/usr/bin/env python

# import re
# import math
# import collections
from copy import deepcopy


DEFAULT_INPUT_FILE = "input/part1.txt"

ASTEROID = '#'


def print_space(s):
	for row in s:
		print("".join(row))

def count_visible_asteroids(asteroids, x, y):
	seen_ratios = { 10: {}, 11: {}, 1: {}, 0: {} }
	seen_larger_x = False
	seen_larger_y = False
	seen_smaller_x = False
	seen_smaller_y = False

	for ax, ay in asteroids:
		if ax == x and ay == y:
			continue
		ox = x - ax
		oy = y - ay

		quadrant_key = (int(ox < 0) * 10) + int(oy < 0)

		if oy == 0 and ax > x:
			if seen_larger_x:
				continue
			seen_larger_x = True
		elif oy == 0 and ax < x:
			if seen_smaller_x:
				continue
			seen_smaller_x = True
		elif ox == 0 and ay > y:
			if seen_larger_y:
				continue
			seen_larger_y = True
		elif ox == 0 and ay < y:
			if seen_smaller_y:
				continue
			seen_smaller_y = True
		else:
			ratio = (ox*1.0)/oy
			if quadrant_key not in seen_ratios:
				raise Exception("seen_ratios missing quadrant_key {}".format(quadrant_key))
			if ratio not in seen_ratios[quadrant_key]:
				seen_ratios[quadrant_key][ratio] = True

	return len(seen_ratios[11]) + len(seen_ratios[10]) + len(seen_ratios[1]) + len(seen_ratios[0]) + \
		int(seen_larger_x) + int(seen_smaller_x) + int(seen_larger_y) + int(seen_smaller_y)


def main(args):
	space = []
	asteroids = {}
	y = 0
	with open(args.file, "r") as fh:
		for line in fh:
			if line.strip() == '':
				pass

			row = []
			for x, c in enumerate(line.strip()):
				if c == ASTEROID:
					asteroids[(x,y)] = True
				row.append(c)
			space.append(row)

			y += 1

	space_copy = deepcopy(space)
	max_visible = 0
	for (x,y) in asteroids:
		count = count_visible_asteroids(asteroids, x, y)
		space_copy[y][x] = str(count)
		if count > max_visible:
			max_visible = count

	print_space(space_copy)

	print("Max visible: {}".format(max_visible))




if __name__ == '__main__':
	import argparse

	parser = argparse.ArgumentParser()
	parser.add_argument('-f', '--file', help='Input file, default: {}'.format(DEFAULT_INPUT_FILE), default=DEFAULT_INPUT_FILE)
	args = parser.parse_args()

	main(args)
