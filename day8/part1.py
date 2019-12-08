#!/usr/bin/env python

# import re
# import math
# import collections

# Wrong answer = 2450

DEFAULT_INPUT_FILE = "input/part1.txt"

def read_image_layers(data, w, h):
	layers = []
	range_start = 0
	range_span = w*h
	n_layers = len(data) / range_span

	for i in range(n_layers):
		layers.append(data[range_start:range_start+range_span])
		range_start += range_span

	return layers	

def main(args):
	with open(args.file, "r") as fh:
		data = fh.read().strip()
		layers = read_image_layers(data, args.width, args.height)

		least_zeros = None
		saved_counts = None
		for i in range(len(layers)):
			counts = {0: 0, 1: 0, 2: 0}
			for n in map(int, layers[i]):
				if n not in counts:
					counts[n] = 1
				else:
					counts[n] += 1

			print("Layer {} has {} zeros (least_zeros = {})".format(i, counts[0], least_zeros))

			if least_zeros is None or counts[0] < least_zeros:
				least_zeros = counts[0]
				saved_counts = counts

		print("Least zeros on a layer: {}".format(counts[0]))
		count_of_ones = saved_counts[1]
		count_of_twos = saved_counts[2]
		print("Zero count layer: count of 1s ({}) * count of 2s ({}) = {}".format(count_of_ones, count_of_twos, count_of_ones * count_of_twos))



if __name__ == '__main__':
	import argparse

	parser = argparse.ArgumentParser()
	parser.add_argument('-f', '--file', help='Input file, default: {}'.format(DEFAULT_INPUT_FILE), default=DEFAULT_INPUT_FILE)
	parser.add_argument('-w', '--width', type=int, help="Image width", default=25)
	parser.add_argument('-H', '--height', type=int, help="Image height", default=6)
	args = parser.parse_args()

	main(args)
