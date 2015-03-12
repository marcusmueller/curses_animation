#!/usr/bin/python2
import curses
import numpy
from time import sleep
n_points  = 9
l_period  = 12
t_refresh = 1.0/20

scr = curses.initscr()
curses.start_color()
logo = open("ettus.logo.nosine.txt").read()

lines = logo.split("\n")
middle, barline = max(enumerate(lines), key=lambda tup: tup[1].count("="))
barlength = barline.count("=")
maxheight = min(middle-1, len(lines)-1-middle) 

total_x = numpy.pi * n_points / (l_period / 2.0)
chr_per_x = barlength/total_x
#chr_per_x = (barlength * l_period) / (numpy.pi*n_points)
#x_per_chr = 2
scr.addstr(0,0,logo)
scr.addstr(middle, 0, barline, curses.COLOR_GREEN)
scr.refresh()
sleep(0.200)
X = numpy.linspace(-total_x/2, total_x/2, n_points)
x_off = 0
while(True):
	Y = numpy.sin(X+x_off)
	to_clear = []
	for x,y in zip(X,Y):
		y_real = int(numpy.round(y * maxheight + middle))
		x_real = int(numpy.round(barlength / 2 + x * chr_per_x))
		scr.addch(y_real, x_real, ord("o"))
		to_clear.append((y_real, x_real))
		lineheight = y_real - middle
		if lineheight < 0:
			for y_stroke in range(y_real+1, middle):
				scr.addch(y_stroke, x_real, ord("|"))
				to_clear.append((y_stroke,x_real))
		elif lineheight > 0:
			for y_stroke in range(middle+1, y_real):
				scr.addch(y_stroke, x_real, ord("|"))
				to_clear.append((y_stroke,x_real))
	scr.refresh()
	scr.addstr(0,0,logo)
	scr.addstr(middle, 0, barline, curses.COLOR_GREEN)
	#for x_clear, y_clear in to_clear:
	#	if y_clear < len(lines) and x_clear < len(lines[y_clear]):
	#		scr.addch(y_clear, x_clear, ord(lines[y_clear][x_clear]))
	sleep(t_refresh)
	x_off += numpy.pi/n_points/3
