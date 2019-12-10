#!/usr/bin/env python

# import re
# import math
# import collections
from copy import deepcopy

# WRONG ANSWER: 2031

DEFAULT_INPUT_FILE = "input/part1.txt"

ASTEROID  = '#'
NORTH     = "north"
NORTHEAST = "northeast"
EAST      = "east"
SOUTHEAST = "southeast"
SOUTH     = "south"
SOUTHWEST = "southwest"
WEST      = "west"
NORTHWEST = "northwest"

DIRECTION_ORDER = [NORTH, NORTHEAST, EAST, SOUTHEAST, SOUTH, SOUTHWEST, WEST, NORTHWEST]

def manhattan_distance(x1, y1, x2, y2):
	return abs(x1 - x2) + abs(y1 - y2)

def print_space(s):
	for row in s:
		print("".join(row))

def get_quadrants(asteroids, x, y):
	quadrant_map = {
		0: NORTHWEST,
		1: SOUTHWEST,
		10: NORTHEAST,
		11: SOUTHEAST
	}
	quadrants = {
		EAST: [],
		WEST: [],
		SOUTH: [],
		NORTH: [],
		NORTHWEST: {},
		SOUTHWEST: {},
		NORTHEAST: {},
		SOUTHEAST: {}
	}

	for ax, ay in asteroids:
		if ax == x and ay == y:
			continue
		ox = x - ax
		oy = y - ay

		quadrant_key = quadrant_map[(int(ox < 0) * 10) + int(oy < 0)]

		if oy == 0 and ax > x:
			quadrants[EAST].append((ax,ay))
		elif oy == 0 and ax < x:
			quadrants[WEST].append((ax,ay))
		elif ox == 0 and ay > y:
			quadrants[SOUTH].append((ax,ay))
		elif ox == 0 and ay < y:
			quadrants[NORTH].append((ax,ay))
		else:
			ratio = (ox*1.0)/oy
			if ratio not in quadrants[quadrant_key]:
				quadrants[quadrant_key][ratio] = []
			quadrants[quadrant_key][ratio].append((ax,ay))

	return quadrants

def get_visible_asteroids(q):
	count = 0
	for k in q:
		if k in [NORTH, EAST, SOUTH, WEST]:
			count += int(len(q[k]) > 0)
		else:
			count += len(q[k])
	return count


def fire_the_lasers(quadrants, x, y, asteroid_count, limit=None):
	# Sort quadrants first
	print("fire_the_lasers called on {}, {}".format(x, y))
	sq = {}

	for k in [NORTH, SOUTH, EAST, WEST]:
		sq[k] = sorted(quadrants[k], key=lambda xy: manhattan_distance(x, y, xy[0], xy[1]))

	for k in [NORTHEAST, SOUTHEAST, SOUTHWEST, NORTHWEST]:
		sq[k] = {}
		for r in quadrants[k]:
			sq[k][r] = sorted(quadrants[k][r], key=lambda xy: manhattan_distance(x, y, xy[0], xy[1]))

	laser_count = 0
	laser_direction_index = 0 # NORTH
	while True:
		coords = None
		laser_direction = DIRECTION_ORDER[laser_direction_index]
		print("# laser_direction -- {}".format(laser_direction))
		if laser_direction in [NORTH, EAST, SOUTH, WEST] and sq[laser_direction]:
			coords = sq[laser_direction].pop(0)
			laser_count += 1
			print("Laser blast #{} hit asteroid at {},{}".format(laser_count, coords[0], coords[1]))
			if limit is not None and laser_count == limit:
				return
			elif asteroid_count - 1 == laser_count:
				print("We blew up all of the asteroids!")
				return

		elif laser_direction in [NORTHEAST, NORTHWEST, SOUTHEAST, SOUTHWEST] and sq[laser_direction]:
			sorted_ratios = sorted(sq[laser_direction].keys(), reverse=True)
			for r in sorted_ratios:
				coords = sq[laser_direction][r].pop(0)
				laser_count += 1
				print("Laser blast #{} hit asteroid at {},{}".format(laser_count, coords[0], coords[1]))
				if limit is not None and laser_count == limit:
					return
				elif asteroid_count - 1 == laser_count:
					print("We blew up all of the asteroids!")
					return

				if len(sq[laser_direction][r]) == 0:
					print("Last under {}, deleting key".format(r))
					sq[laser_direction].pop(r, None)

		# Move the laser to the next direction
		laser_direction_index = (laser_direction_index + 1) % len(DIRECTION_ORDER)


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
	saved_quadrant = None
	saved_x = None
	saved_y = None
	for (x,y) in asteroids:
		quadrants = get_quadrants(asteroids, x, y)
		count = get_visible_asteroids(quadrants)
		space_copy[y][x] = str(count)
		if count > max_visible:
			max_visible = count
			saved_quadrant = quadrants
			saved_x = x
			saved_y = y

	print("Max visible: {}, located at {},{}".format(max_visible, saved_x, saved_y))

	fire_the_lasers(saved_quadrant, saved_x, saved_y, asteroid_count=len(asteroids), limit=200)




if __name__ == '__main__':
	import argparse

	parser = argparse.ArgumentParser()
	parser.add_argument('-f', '--file', help='Input file, default: {}'.format(DEFAULT_INPUT_FILE), default=DEFAULT_INPUT_FILE)
	args = parser.parse_args()

	main(args)
