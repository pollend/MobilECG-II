#!/usr/bin/python

import cv2
import sys
import numpy as np 

if len(sys.argv)<2:
	sys.stderr.write("Usage: "+sys.argv[0]+" <image file>\n")
	sys.exit(-1)

img=cv2.imread(sys.argv[1], cv2.IMREAD_GRAYSCALE)
if img is None:
	sys.stderr.write("Invalid input file: "+sys.argv[1]+"\n")
	sys.exit(-1)

if img.shape[0]!=64 or img.shape[1]!=128:
	sys.stderr.write("Input image should be 128x64.\n")
	sys.exit(-1)

data=np.zeros(int(img.shape[0]*img.shape[1]/8), np.uint8)
for y in range(img.shape[0]):
	for x in range(img.shape[1]):
		if img[y,x]>0.5:
			offset=y*img.shape[1]+x
			data[offset >> 3] |= 1 << (offset & 7)

sys.stdout.write("#include \"image.hpp\"\n\n")
sys.stdout.write("static const uint8_t image[] = {")

for a in range(data.shape[0]):
	if a % 16==0:
		sys.stdout.write("\n\t");
	
	sys.stdout.write("0x%.2X, " % data[a])
	
sys.stdout.write("\n};\n\n")
sys.stdout.write("const Image imgObject(image, %d, %d);\n\n" % (img.shape[1], img.shape[0]))
