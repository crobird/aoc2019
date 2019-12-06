#!/usr/bin/env python

# import re
# import math
# import collections


DEFAULT_INPUT_FILE = "input/part1.txt"

class Planet(object):
	def __init__(self, name):
		self.name      = name
		self.parent    = None
		self.children  = []

	def __repr__(self):
		return "{} ) {}".format(self.name, ",".join([x.name for x in self.children]))

class System(object):
	def __init__(self):
		self.planets = {}

	def get_planet(self, name):
		if name in self.planets:
			return self.planets[name]
		p = Planet(name)
		self.planets[name] = p
		return p

	def get_direct_orbit_count(self):
		if "COM" in self.planets:
			return len(self.planets) - 1
		return len(self.planets)

	def get_indirect_orbit_count(self, name="COM", level=0):
		kid_total = 0
		for c in self.planets[name].children:
			kid_total += self.get_indirect_orbit_count(c.name, level+1)
		indirect = level - 1 if name != 'COM' else 0
		return kid_total + indirect



def main(args):
	s = System()
	with open(args.file, "r") as fh:
		for line in fh:
			if line.strip() == '':
				pass

			a,b = line.strip().split(')')
			planet_a = s.get_planet(a)
			planet_b = s.get_planet(b)
			planet_b.parent = planet_a
			planet_a.children.append(planet_b)

	direct_orbit_count = s.get_direct_orbit_count()
	indirect_orbit_count = s.get_indirect_orbit_count()
	print("direct + indirect count = {}".format(direct_orbit_count + indirect_orbit_count))


if __name__ == '__main__':
	import argparse

	parser = argparse.ArgumentParser()
	parser.add_argument('-f', '--file', help='Input file, default: {}'.format(DEFAULT_INPUT_FILE), default=DEFAULT_INPUT_FILE)
	args = parser.parse_args()

	main(args)
