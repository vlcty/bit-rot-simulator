#!/usr/bin/python
#
# MIT License
#
# Copyright (c) 2021 Josef 'veloc1ty' Stautner
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# -------------------------------------------------------------------------------
# bitrot.py
#
# My simple approach to simulate bitrot and/or a failing harddrive. What it does:
#
# 1) Open specified partition
# 2) Seek between X and Y bytes (variable "rot_offset_range")
# 3) Write Y random bytes on that position (variable "bytes_to_rot")
# 4) Repeat step 2 and 3 until end of target is reached
#
# -------------------------------------------------------------------------------
#
# Settings for you to play with:
#

# Skip between X and Y bytes after each write.
# Depending on your partition size tweak these values to your needs.
#                    4 MBytes  20 MBytes
rot_offset_range = [ 1024 * 4, 1024 * 20 ]

# Write X bytes of random data each write
# I suggest keeping this value small!
bytes_to_rot = 4

#
# -------------------------------------------------------------------------------
#
import sys
from random import randrange, randbytes

partition = ""

if len(sys.argv) != 2:
	print("Usage: ./bitrot.py /path/to/partition")
	exit(1)
else:
	partition = sys.argv[1]

print("Warning: Random bytes will be written to {0}! Are you sure you want to continue?".format(partition))

if input("Please type uppercase YES if you know what you are doing: ") != "YES":
	print("Doing nothing!")
	exit(0)

partition_to_rot = None

try:
	partition_to_rot = open(partition, "wb")
except Exception as e:
	print("Error opening partition: {}".format(e))
	exit(1)

partition_to_rot.seek(0, 2) # Seek to the end of the file
partition_to_rot_end = partition_to_rot.tell()
partition_to_rot.seek(0, 0) # Seek back to the beginning

counter = 0
next_offset = randrange(rot_offset_range[0], rot_offset_range[1], 1) # Calculate a random offset
print_progress_after_N_writes = 10 * 1000 * 5
progress_note = "Position: {}/{} -> {}% done"

print(progress_note.format(0, partition_to_rot_end, round(0.0,2)))

while partition_to_rot.tell() + next_offset + bytes_to_rot < partition_to_rot_end:
	try:
		partition_to_rot.seek(next_offset, 1) # Seek to offset relative to current position
		partition_to_rot.write(randbytes(bytes_to_rot)) # Rot the bits!
		next_offset = randrange(rot_offset_range[0], rot_offset_range[1], 1)
		counter += 1

		if counter == print_progress_after_N_writes:
			counter = 0
			current_position = partition_to_rot.tell()
			percent_done = ( current_position / partition_to_rot_end ) * 100

			print(progress_note.format(current_position, partition_to_rot_end, round(percent_done, 2)))

	except Exception as e:
		print("Unexpected error: {}".format(e))
		break

print(progress_note.format(partition_to_rot_end, partition_to_rot_end, round(100.0,2)))

partition_to_rot.close()
