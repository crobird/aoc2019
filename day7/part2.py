#!/usr/bin/env python

import re
# import math
# import collections
from copy import copy
from itertools import permutations

# Wrong answer: 41583


DEFAULT_INPUT_FILE = "input/part1.txt"

class Stack(object):
	def __init__(self, l=None):
		self.l = l or []

	def __repr__(self):
		return str(self.l)

	def pop(self):
		return self.l.pop(0)

	def push(self, v):
		self.l.insert(0, v)

class Computer(object):
	def __init__(self, name, instructions, setting=None, debug=False):
		self.name = name
		self.instructions = instructions
		self.setting = setting
		self.io_in = []
		self.io_out = []
		self.debug = debug
		self.index = 0
		if setting:
			self.apply_setting()

	def __repr__(self):
		return """
		{}: 
			instructions={}
			io_in={}
			io_out={}
			index={}
""".format(self.name, self.instructions, self.io_in, self.io_out, self.index)

	def pop(self, l):
		if not l:
			return None
		return l.pop()

	def add_input(self, v):
		self.io_in.insert(0, v)

	def get_input(self):
		return self.pop(self.io_in)

	def add_output(self, v):
		self.io_out.insert(0, v)

	def get_output(self):
		return self.pop(self.io_out)

	def apply_setting(self):
		if self.io_in:
			raise Exception("Trying to apply setting of {} for Computer {}, but the input buffer already has data {}".format(self.setting, self.name, self.io_in))
		self.add_input(self.setting)

	def get_param_value(self, param_value, mode):
		if mode == '0':
			return self.instructions[param_value]
		elif mode == '1':
			return param_value
		else:
			raise Exception("unexpected mode passed to get_param_value: param_value = {}, mode = {}".format(param_value, mode))

	def debug_instruction(self, l, input_value=None):
		if self.debug:
			s = """
		operator_string: {}
		code: {}
		modes: {}
		params: {}
		------------
		""".format(*l)
			if input_value:
				s = "		input: {}".format(input_value) + s
			print(s)

	def debug_print(self, s):
		if self.debug:
			print(s)

	def get_params(self, n):
		return [self.instructions[self.index+i] for i in range(1,n+1)]

	def go(self):
		self.debug_print("{}: STARTING ON INSTRUCTION {}".format(self.name, self.index))
		halted = False
		while True:
			operator_string = "{:05d}".format(self.instructions[self.index])
			code = int(operator_string[-2:])
			modes = operator_string[:3]

			if code == 99:
				halted = True
				self.debug_print("{}: HALTING".format(self.name))
				break

			param_count = 0
			instruction_pointer = None

			if code == 1:
				# -- ADDITION
				param_count = 3
				params = self.get_params(param_count)
				self.debug_instruction([operator_string, code, modes, params])
				a = self.get_param_value(params[0], modes[2])
				b = self.get_param_value(params[1], modes[1])
				self.instructions[params[2]] = a + b
			elif code == 2:
				# -- MULTIPLICATION
				param_count = 3
				params = self.get_params(param_count)
				self.debug_instruction([operator_string, code, modes, params])
				a = self.get_param_value(params[0], modes[2])
				b = self.get_param_value(params[1], modes[1])
				self.instructions[params[2]] = a * b
			elif code == 3:
				# INPUT COPY
				input_value = self.get_input()
				if input_value is None:
					# No input for us, give control back
					self.debug_print("{}: NO INPUT - STOPPING ON INSTRUCTION {}".format(self.name, self.index))
					break
				param_count = 1
				params = self.get_params(param_count)
				self.debug_instruction([operator_string, code, modes, params], input_value)
				self.instructions[params[0]] = input_value
			elif code == 4:
				# OUTPUT
				param_count = 1
				params = self.get_params(param_count)
				self.debug_instruction([operator_string, code, modes, params])
				a = self.get_param_value(params[0], modes[2])
				self.add_output(a)
			elif code == 5:
				# JUMP IF TRUE
				param_count = 2
				params = self.get_params(param_count)
				self.debug_instruction([operator_string, code, modes, params])
				a = self.get_param_value(params[0], modes[2])
				b = self.get_param_value(params[1], modes[1])
				if a:
					instruction_pointer = b
			elif code == 6:
				# JUMP IF FALSE
				param_count = 2
				params = self.get_params(param_count)
				self.debug_instruction([operator_string, code, modes, params])
				a = self.get_param_value(params[0], modes[2])
				b = self.get_param_value(params[1], modes[1])
				if not a:
					instruction_pointer = b
			elif code == 7:
				# LESS THAN
				param_count = 3
				params = self.get_params(param_count)
				self.debug_instruction([operator_string, code, modes, params])
				a = self.get_param_value(params[0], modes[2])
				b = self.get_param_value(params[1], modes[1])
				self.instructions[params[2]] = 1 if a < b else 0
				pass
			elif code == 8:
				# EQUALS
				param_count = 3
				params = self.get_params(param_count)
				self.debug_instruction([operator_string, code, modes, params])
				a = self.get_param_value(params[0], modes[2])
				b = self.get_param_value(params[1], modes[1])
				self.instructions[params[2]] = 1 if a == b else 0

			self.index = instruction_pointer if instruction_pointer is not None else self.index + 1 + param_count
		return halted

def link_computers(computers):
	for i in range(len(computers)):
		next_i = (i+1) % len(computers)
		computers[i].io_out = computers[next_i].io_in

def run_pipeline(instructions, order, starting_input=0, debug=False):
	# Build computers A-E
	computers = [Computer(name=chr(65+i), instructions=copy(instructions), setting=order[i], debug=debug) for i in range(len(order))]
	computers[0].add_input(starting_input)

	link_computers(computers)

	active_index = 0
	halted_computers = []
	while True:
		if active_index in halted_computers:
			raise Exception("Calling Computer {}, but it's halted".format(computers[active_index].name))
		if not computers[active_index].io_in:
			raise Exception("Calling Computer {}, but there's nothing in the input buffer".format(computers[active_index].name))

		halted = computers[active_index].go()
		if halted and active_index == len(computers) - 1:
			return computers[active_index].get_output()
		elif halted:
			halted_computers.append(active_index)

		active_index = (active_index + 1) % len(computers)


def main(args):
	with open(args.file, "r") as fh:
		for line in fh:
			if line.strip() == '':
				pass
			x = map(int, line.split(','))

	all_perms = list(permutations([5,6,7,8,9]))
	max_result = None
	for p in all_perms:
		out = run_pipeline(x, p, debug=args.debug)
		if max_result is None or out > max_result:
			max_result = out

	print("Max output is {}".format(max_result))


if __name__ == '__main__':
	import argparse

	parser = argparse.ArgumentParser()
	parser.add_argument('-f', '--file', help='Input file, default: {}'.format(DEFAULT_INPUT_FILE), default=DEFAULT_INPUT_FILE)
	parser.add_argument('-d', '--debug', default=False, action="store_true", help="Debug info")
	args = parser.parse_args()

	main(args)
