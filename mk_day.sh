#!/usr/bin/env bash

if [ $# -eq 0 ]
  then
    echo "No arguments supplied"
    exit 1
fi

daydir="day$1"
mkdir -p $daydir/input
touch $daydir/input/part1.txt
touch $daydir/input/part2.txt

cat > $daydir/part1.py <<'EOF'
#!/usr/bin/env python

DEFAULT_INPUT_FILE = "input/part1.txt"

def main(args):
	with open(args.file, "r") as fh:
		for line in fh:
			if line.strip() == '':
				pass
			mobj = re.match(r'', line)
			if mobj:
				print(mobj)

if __name__ == '__main__':
	import argparse

	parser = argparse.ArgumentParser()
	parser.add_argument('-f', '--file', help='Input file, default: {}'.format(DEFAULT_INPUT_FILE), default=DEFAULT_INPUT_FILE)
	args = parser.parse_args()

	main(args)
EOF
cp $daydir/part1.py $daydir/part2.py
chmod a+x $daydir/*.py
