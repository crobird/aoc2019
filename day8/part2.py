#!/usr/bin/env python

# import re
# import math
# import collections
from copy import copy

# Wrong answer = 2450

DEFAULT_INPUT_FILE = "input/part1.txt"

def read_image_layers(data, w, h):
	range_start = 0
	range_span = w*h
	n_layers = len(data) / range_span
	layers = [None for i in range(n_layers)]

	for i in range(n_layers):
		layers[i] = [None for x in range(h)]
		layer_str = data[range_start:range_start+range_span]
		layer_start_range = 0
		for y in range(h):
			layers[i][y] = map(int, layer_str[layer_start_range:layer_start_range+w])
			layer_start_range += w
		range_start += range_span
	return layers	

def print_image(image):
	pixel_map = [' ', '#', '-']
	for row in image:
		print("".join([pixel_map[i] for i in row]))

def main(args):
	with open(args.file, "r") as fh:
		data = fh.read().strip()
		layers = read_image_layers(data, args.width, args.height)

		image = copy(layers[0])
	
		for l in range(1,len(layers)):
			for y, row in enumerate(layers[l]):
				for x,v in enumerate(row):
					if image[y][x] == 2 and layers[l][y][x] != 2:
						image[y][x] = layers[l][y][x]

		print_image(image)

if __name__ == '__main__':
	import argparse

	parser = argparse.ArgumentParser()
	parser.add_argument('-f', '--file', help='Input file, default: {}'.format(DEFAULT_INPUT_FILE), default=DEFAULT_INPUT_FILE)
	parser.add_argument('-w', '--width', type=int, help="Image width", default=25)
	parser.add_argument('-H', '--height', type=int, help="Image height", default=6)
	args = parser.parse_args()

	main(args)
