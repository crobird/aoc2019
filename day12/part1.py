#!/usr/bin/env python

import re
# import math
# import collections
from itertools import permutations

# Wrong answer: 183

DEFAULT_INPUT_FILE = "input/part1.txt"
DEFAULT_STEPS = 5


class Moon(object):
	def __init__(self, name, x, y, z):
		self.name = name
		self.x = x
		self.y = y
		self.z = z
		self.xv = 0
		self.yv = 0
		self.zv = 0
		self.xc = 0
		self.yc = 0
		self.zc = 0

	def __repr__(self):
		return "name={}, pos=<x={}, y={}, z={}>, vel=<xv={}, yv={}, zv={}>".format(self.name, self.x, self.y, self.z, self.xv, self.yv, self.zv)

	def get_change(self, a, b):
		if a < b:
			return 1
		elif a > b:
			return -1
		return 0

	def apply_gravity_changes(self):
		self.xv += self.xc
		self.yv += self.yc
		self.zv += self.zc
		self.xc = 0
		self.yc = 0
		self.zc = 0

	def add_gravity_changes(self, other_moon):
		self.xc += self.get_change(self.x, other_moon.x)
		self.yc += self.get_change(self.y, other_moon.y)
		self.zc += self.get_change(self.z, other_moon.z)

	def apply_velocity(self):
		self.x += self.xv
		self.y += self.yv
		self.z += self.zv

	@property
	def total_energy(self):
		return self.potential_energy * self.kinetic_energy
	
	@property
	def potential_energy(self):
		return abs(self.x) + abs(self.y) + abs(self.z)

	@property
	def kinetic_energy(self):
		return abs(self.xv) + abs(self.yv) + abs(self.zv)


def print_moons(moons, step = 0):
	print("Step: {}".format(step))
	for m in moons:
		print(m)

def main(args):
	moons = []
	with open(args.file, "r") as fh:
		moon_count = 0
		for line in fh:
			if line.strip() == '':
				pass
			mobj = re.match(r'<x=(\-?\d+), y=(\-?\d+), z=(\-?\d+)>', line)
			if mobj:
				moon_count += 1
				moons.append(Moon(str(moon_count), int(mobj.group(1)), int(mobj.group(2)), int(mobj.group(3))))


	moon_perms = list(permutations(moons, 2))
	if args.debug:
		print_moons(moons)
	for n in range(1, args.steps+1):
		for (m1, m2) in moon_perms:
			m1.add_gravity_changes(m2)
		for m in moons:
			m.apply_gravity_changes()
			m.apply_velocity()
		if args.debug:
			print_moons(moons, n)

	if args.debug:
		for m in moons:
			print(m)
			print("potential_energy: {}, kinetic_energy: {}, total_energy: {}".format(m.potential_energy, m.kinetic_energy, m.total_energy))
	print("Sum of total energy = {}".format(sum([m.total_energy for m in moons])))		

if __name__ == '__main__':
	import argparse

	parser = argparse.ArgumentParser()
	parser.add_argument('-f', '--file', help='Input file, default: {}'.format(DEFAULT_INPUT_FILE), default=DEFAULT_INPUT_FILE)
	parser.add_argument('-s', '--steps', help="number of steps, default: {}".format(DEFAULT_STEPS), type=int, default=DEFAULT_STEPS)
	parser.add_argument('-d', '--debug', help="debug", default=False, action="store_true")
	args = parser.parse_args()

	main(args)
