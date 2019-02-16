import sys

if len(sys.argv) < 2:
	print("Usage: Provide a file for you to verify board placement of")
	sys.exit(0)

class Verify_tile:

	def __init__(self, str):
		if str[0] == "F":
			self.size = "F"
			self.booth_num = None
		elif str[0] == "B":
			self.size = "B"
			self.booth_num = None
		elif str[0] == "L":
			self.size = "L"
			self.booth_num = int(str[1:])
		elif str[0] == "M":
			self.size = "M"
			self.booth_num = int(str[1:])
		elif str[0] == "S":
			self.size = "S"
			self.booth_num = int(str[1:])
		elif str[0] == "E":
			self.size = "E"
			self.booth_num = int(str[1:])
		else:
			self.size = ""
			self.booth_num = int(str)

	def get_num(self):
		return self.booth_num

	def is_end(self):
		return self.size == "E"

	def is_booth(self):
		return self.size == "L" or self.size == "M" or self.size == "S"

	def is_line(self):
		return self.size == ""

	def is_free_space(self):
		return self.booth_num == None

board = []
height = 0
width = 0
num_booths = 0
num_bots = 0

with open(sys.argv[1], "r") as f:
	dim = f.readline()
	dims = dim.split()

	height = int(dims[0])
	width = int(dims[1])
	num_booths = int(dims[2])
	num_bots = int(dims[3])

	for line in f:
		row = []

		for item in line.split():
			row.append(Verify_tile(item))

		board.append(row)

if len(board) != height:
	print("Height {} doesn't match board length {}".format(height, len(board)))

for count, row in enumerate(board):
	if len(row) != width:
		print("Width at {} value {} doesn't match board width {}".format(count, width, len(row)))

def verify_nums():
	# here we are checking if all the booths are numbered correctly
	booth_seen = set()
	line_seen = set()
	endof_line_seen = set()

	for x, row in enumerate(board):
		for y, tile in enumerate(row):
			if tile.is_booth():
				num = tile.get_num()
				if not (0 <= num < num_booths):
					return "Booth num {} outside range [{} {})".format(num, 0, num_booths)
				booth_seen.add(num)
			elif tile.is_end():
				num = tile.get_num()
				if not (0 <= num < num_booths):
					return "End num {} outside range [{}, {})".format(num, 0, num_booths)
				endof_line_seen.add(num)
			elif tile.is_line():
				num = tile.get_num()
				if not (0 <= num < num_booths):
					return "Line num {} outside range [{}, {})".format(num, 0, num_booths)
				line_seen.add(num)
			elif tile.is_free_space():
				continue
			else:
				return "Don't recognize this tile {} at {} {}".format(str(tile), x, y)

	# verification
	for x in range(0, num_booths):
		if not (x in booth_seen):
			return "Missing booth {} from map".format(x)
		if not (x in line_seen):
			return "Missing line {} from map".format(x)
		if not (x in endof_line_seen):
			return "Missing end {} from map".format(x)

	return ""

print(verify_nums())
print("Looks like it passed everything")
