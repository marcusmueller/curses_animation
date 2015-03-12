#!/usr/bin/python2
import curses
import numpy
from time import sleep
import argparse


parser = argparse.ArgumentParser("Animation!")
parser.add_argument("-L","--logo", default="ettus.logo.nosine.txt", type=argparse.FileType("r"))
parser.add_argument("-n","--n_points", default=9, type=int)
parser.add_argument("-l","--l_period", default=12, type=int)
parser.add_argument("-f","--frequency", default=1.0/3, type=float)
parser.add_argument("-r","--refresh", default = 1.0/20, type=float)
args = parser.parse_args()

n_points = args.n_points
l_period  = args.l_period
t_refresh = args.refresh
freq = args.frequency
logo = args.logo.read()


scr = curses.initscr()
curses.start_color()
curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_WHITE)
scr.attroff(curses.A_COLOR)
scr.attron(curses.color_pair(1))
curses.noecho()

lines = logo.split("\n")
middle, barline = max(enumerate(lines), key=lambda tup: tup[1].count("="))
barlength = barline.count("=")-2
maxheight = min(middle-1, len(lines)-1-middle) 

total_x = numpy.pi * n_points / (l_period / 2.0)
chr_per_x = barlength/total_x
#chr_per_x = (barlength * l_period) / (numpy.pi*n_points)
#x_per_chr = 2
scr.addstr(0,0,logo)
scr.attron(curses.color_pair(2))
scr.addstr(middle, 0, barline)
scr.attron(curses.color_pair(1))
scr.refresh()
sleep(0.200)
X = numpy.linspace(-total_x/2, total_x/2, n_points)
x_off = 0
while(True):
	Y = numpy.sin(X+x_off)
	scr.attron(curses.color_pair(2))
	scr.addstr(middle, 0, barline)
	for x,y in zip(X,Y):
		y_real = int(numpy.round(y * maxheight + middle))
		x_real = int(numpy.round(barlength / 2 + x * chr_per_x))
		scr.addch(y_real, x_real, ord("o"))
		lineheight = y_real - middle
		if lineheight < 0:
			for y_stroke in range(y_real+1, middle):
				scr.addch(y_stroke, x_real, ord("|"))
		elif lineheight > 0:
			for y_stroke in range(middle+1, y_real):
				scr.addch(y_stroke, x_real, ord("|"))
	scr.refresh()
	scr.attron(curses.color_pair(1))
	scr.addstr(0,0,logo)
	sleep(t_refresh)
	x_off += numpy.pi * 2 * freq * t_refresh
