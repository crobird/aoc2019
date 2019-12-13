#!/usr/bin/env python

from copy import copy
from itertools import permutations
from enum import Enum


DEFAULT_INPUT_FILE = "input/part1.txt"

MOVE_MAP = dict(
	UP    = (0, -1),
	RIGHT = (1, 0),
	DOWN  = (0, 1),
	LEFT  = (-1, 0)
)

class TileType(Enum):
	EMPTY = 0
	WALL = 1
	BLOCK = 2
	HORIZONTAL_PADDLE = 3
	BALL = 4

class Color(Enum):
	BLACK = 0
	WHITE = 1

class Turns(Enum):
	LEFT  = 0
	RIGHT = 1

class Orientation(Enum):
	UP    = 0
	RIGHT = 1
	DOWN  = 2
	LEFT  = 3

	def left_turn(self):
		return (self.value + 4 - 1) % 4

	def right_turn(self):
		return (self.value + 1) % 4

	def turn(self, turn_type):
		if turn_type == Turns.LEFT:
			return self.left_turn()
		return self.right_turn()

class Tile(object):
	def __init__(self, x, y , tile_type):
		self.x = x
		self.y = y
		self.type = tile_type

	def __repr__(self):
		return "x={}, y={}, type={}".format(self.x, self.y, self.type)

class Panel(object):
	def __init__(self, x, y, color):
		self.x = x
		self.y = y
		self.color = color
		self.painted = False

	def paint(self, color):
		self.color = color
		self.painted = True


class Computer(object):
	def __init__(self, name, instructions, setting=None, debug=False):
		self.name = name
		self.instructions = instructions
		self.setting = setting
		self.io_in = []
		self.io_out = []
		self.debug = debug
		self.index = 0
		self.relative_base = 0
		self.extended_memory = {}
		if setting is not None:
			self.apply_setting()

	def __repr__(self):
		return """
		{}: 
			instructions={}
			io_in={}
			io_out={}
			relative_base={}
			index={}
""".format(self.name, self.instructions, self.io_in, self.io_out, self.relative_base, self.index)

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
			return self.get_instruction_value(param_value)
		elif mode == '1':
			return param_value
		elif mode == '2':
			 return self.get_instruction_value(param_value + self.relative_base)
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

	def set_instruction_value(self, location, mode, v):
		if mode == '2':
			location += self.relative_base

		if location < len(self.instructions):
			self.instructions[location] = v
		else:
			self.extended_memory[location] = v

	def get_instruction_value(self, location):
		if location < len(self.instructions):
			return self.instructions[location]
		elif location in self.extended_memory:
			return self.extended_memory[location]
		else:
			return 0

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
				self.set_instruction_value(params[2], modes[0], a+b)
			elif code == 2:
				# -- MULTIPLICATION
				param_count = 3
				params = self.get_params(param_count)
				self.debug_instruction([operator_string, code, modes, params])
				a = self.get_param_value(params[0], modes[2])
				b = self.get_param_value(params[1], modes[1])
				self.set_instruction_value(params[2], modes[0], a*b)
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
				self.set_instruction_value(params[0], modes[2], input_value)
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
				self.set_instruction_value(params[2], modes[0], 1 if a < b else 0)
			elif code == 8:
				# EQUALS
				param_count = 3
				params = self.get_params(param_count)
				self.debug_instruction([operator_string, code, modes, params])
				a = self.get_param_value(params[0], modes[2])
				b = self.get_param_value(params[1], modes[1])
				self.set_instruction_value(params[2], modes[0], 1 if a == b else 0)
			elif code == 9:
				# RELATIVE BASE OFFSET
				param_count = 1
				params = self.get_params(param_count)
				self.debug_instruction([operator_string, code, modes, params])
				a = self.get_param_value(params[0], modes[2])
				self.relative_base += a

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

def move_forward(x, y, dir):
	adds = MOVE_MAP[dir.name]
	return (x + adds[0], y + adds[1])

def draw(panels):
	min_x = min(panels, key=lambda x: x[0])[0]
	min_y = min(panels, key=lambda x: x[1])[1]
	max_x = max(panels, key=lambda x: x[0])[0]
	max_y = max(panels, key=lambda x: x[1])[1]

	n_rows = max_y - min_y + 1
	n_cols = max_x - min_x + 1
	x_offset = min_x * -1
	y_offset = min_y * -1

	canvas = [['.' for x in range(n_cols + 1)] for y in range(n_rows + 1)]
	for k in panels:
		p = panels[k]
		if p.color == Color.WHITE:
			canvas[p.y + y_offset][p.x + x_offset] = '#'

	for row in canvas:
		print("".join(row))


def play_game(game):
	pass

def main(args):
	with open(args.file, "r") as fh:
		for line in fh:
			if line.strip() == '':
				pass
			instructions = map(int, line.split(','))

	computer = Computer(name="A", instructions=copy(instructions), debug=args.debug)

	halted = computer.go()
	if not halted:
		raise Exception("Computer stopped looking for input")

	output = computer.io_out
	output.pop(0)
	tiles = []
	print("length of output: {}".format(len(output)))
	while output:
		if len(output) < 3:
			print("Not enough output values to make another tile: {}".format(output))
			break
		x = int(output.pop(0))
		y = int(output.pop(0))
		tile_type = TileType(int(output.pop(0)))
		tile = Tile(x, y, tile_type)
		print("Tile: {} (len(output) = {})".format(tile, len(output)))
		tiles.append(tile)

	max_x = max([z.x for z in tiles])
	min_x = min([z.x for z in tiles])
	max_y = max([z.y for z in tiles])
	min_y = min([z.y for z in tiles])

	print("min_x = {}, max_x = {}, min_y = {}, max_y = {}".format(min_x, max_x, min_y, max_y))

	game = [[Tile(None, None, TileType(0)) for zz in range(min_x, max_x+1)] for z in range(min_y, max_y+1)]
	for t in tiles:
		if t.type == TileType.EMPTY:
			continue
		game[t.y][t.x] = t.type

	# play_game(game)

	block_total = 0
	for row in game:
		block_total += row.count(TileType.BLOCK)

	print("Game ends with {} blocks".format(block_total))


if __name__ == '__main__':
	import argparse

	parser = argparse.ArgumentParser()
	parser.add_argument('-f', '--file', help='Input file, default: {}'.format(DEFAULT_INPUT_FILE), default=DEFAULT_INPUT_FILE)
	parser.add_argument('-d', '--debug', default=False, action="store_true", help="Debug info")
	args = parser.parse_args()

	main(args)
