#!/usr/bin/env python

import re
# import math
# import collections
from itertools import permutations
from fractions import gcd

# Wrong answer: 9172794540

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

def get_factors(n):
	f = []
	for i in range(2,n):
		if n % i == 0:
			f.append(i)
	return f

def is_prime(n):
	for i in range(2,n):
		if n % i == 0:
			return False
	return True

def get_lcm(nums):
	max_values = {}
	for i in nums:
		factors = get_factors(i)
		prime_factors = filter(is_prime, factors)
		for pf in set(prime_factors):
			c = prime_factors.count(pf)
			if pf not in max_values or c > max_values[pf]:
				max_values[pf] = c

	x = [k * v for k,v in max_values.items()]
	lcm = 1
	for n in x:
		lcm *= n

	return lcm

def main(args):
	moons = []
	with open(args.file, "r") as fh:
		moon_count = 0
		for line in fh:
			if line.strip() == '':
				pass
			mobj = re.match(r'<x=(\-?\d+), y=(\-?\d+), z=(\-?\d+)>', line)
			if mobj:
				moons.append(Moon(str(moon_count), int(mobj.group(1)), int(mobj.group(2)), int(mobj.group(3))))
				moon_count += 1


	moon_perms = list(permutations(moons, 2))
	if args.debug:
		print_moons(moons)

	initial_locations = [(m.x, m.y, m.z, m.xv, m.yv, m.zv) for m in moons]
	previous_locations = [{(m.x, m.y, m.z, m.xv, m.yv, m.zv): 0} for m in moons]
	cycle_steps = [None for x in moons]
	count_cycles = [0 for x in moons]
	freq_counts = [{(m.x, m.y, m.z, m.xv, m.yv, m.zv): 0} for m in moons]
	step_count = 0
	while True:
		step_count += 1
		for (m1, m2) in moon_perms:
			m1.add_gravity_changes(m2)
		for i,m in enumerate(moons):
			m.apply_gravity_changes()
			m.apply_velocity()
			if cycle_steps[i] is None or count_cycles[i] < 100:
				p = (m.x, m.y, m.z, m.xv, m.yv, m.zv)
				# if p == initial_locations[i]:
				# 	print("Got back to initial location for moon {} at step {}".format(m.name, step_count))
				# 	cycle_steps[i] = step_count
				if p in previous_locations[i]:
					print("Hit previous location (from step {}) for moon {} at step {}: {}".format(previous_locations[i][p], m.name, step_count, p))
					cycle_steps[i] = step_count
					count_cycles[i] += 1
					freq_counts[i][p] += 1
				else:
					previous_locations[i][p] = step_count
					freq_counts[i][p] = 1

		if all(cycle_steps) and all([bool(q >= 100) for q in count_cycles]):
			break

		if args.debug:
			print_moons(moons, n)

	for n,m in enumerate(moons):		
		print("cycle steps for {}: {}".format(m.name, cycle_steps[n]))
		foo = filter(lambda x: x[1] > 1, freq_counts[n])
		print("freq_counts for {}: {}".format(m.name, foo))


	# lcm = get_lcm(cycle_steps)
	# print("LCM: {}".format(lcm))


if __name__ == '__main__':
	import argparse

	parser = argparse.ArgumentParser()
	parser.add_argument('-f', '--file', help='Input file, default: {}'.format(DEFAULT_INPUT_FILE), default=DEFAULT_INPUT_FILE)
	parser.add_argument('-s', '--steps', help="number of steps, default: {}".format(DEFAULT_STEPS), type=int, default=DEFAULT_STEPS)
	parser.add_argument('-d', '--debug', help="debug", default=False, action="store_true")
	parser.add_argument('-T', '--test_cycle', help="Planet index to test cycling on", type=int)
	args = parser.parse_args()

	main(args)
