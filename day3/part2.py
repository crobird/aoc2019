#!/usr/bin/env python

# import re
# import math
# import collections


DEFAULT_INPUT_FILE = "input/part1.txt"

DIRECTION_OFFSETS = dict(
	R = [1,0],
	L = [-1,0],
	U = [0,1],
	D = [0,-1]
)

def manhattan_distance(coords):
	return abs(coords[0]) + abs(coords[1])


def coords(instructions):
	cmds = instructions.split(',')
	x = 0
	y = 0
	out = []
	for c in cmds:
		direction = c[0]
		amount = int(c[1:])
		# print("direction: {}, amount: {}".format(direction, amount))
		for i in range(1,amount+1):
			x += DIRECTION_OFFSETS[direction][0]
			y += DIRECTION_OFFSETS[direction][1]
			out.append((x, y))
	return out

def coord_count(instructions, intersection):
	cmds = instructions.split(',')
	x = 0
	y = 0
	count = 0
	for c in cmds:
		direction = c[0]
		amount = int(c[1:])
		for i in range(1,amount+1):
			count += 1
			x += DIRECTION_OFFSETS[direction][0]
			y += DIRECTION_OFFSETS[direction][1]
			if (x,y) == intersection:
				return count

def main(args):
	with open(args.file, "r") as fh:
		lines = [x.strip() for x in fh]
	wire1 = coords(lines[0])
	wire2 = coords(lines[1])

	shared_coords = set(wire1) & set(wire2)
	shortest_distance = None
	best_coords = None
	for sc in shared_coords:
		distance = coord_count(lines[0], sc) + coord_count(lines[1], sc)
		if shortest_distance is None or distance < shortest_distance:
			shortest_distance = distance
			best_coords = sc

	print("The best coords are {}, which have a distance of {}".format(best_coords, shortest_distance))


if __name__ == '__main__':
	import argparse

	parser = argparse.ArgumentParser()
	parser.add_argument('-f', '--file', help='Input file, default: {}'.format(DEFAULT_INPUT_FILE), default=DEFAULT_INPUT_FILE)
	args = parser.parse_args()

	main(args)
