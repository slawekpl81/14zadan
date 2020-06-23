import sys, argparse
import numpy as np 
import math, turtle
from PIL import Image
from datetime import datetime
from math import gcd

from SpiroAnimator import SpiroAnimator
from Spiro import Spiro

def saveDrawing():
# 	turtle.hideturtle()
# 	dateStr = (datetime.now()).strftime("%d%b%Y-%H%M%S")
# 	fileName = 'spiro-' + dateStr
# 	print('saved to file')
#
# 	canvas = turtle.getcanvas()
# 	canvas.postscript(file=fileName+'.eps')
# 	img = Image.open(fileName+'.eps')
# 	img.save(fileName+'.png', 'png')
 	turtle.showturtle()

if __name__ == '__main__':

	print('generate spiro..')
	descStr = """ """

	parser = argparse.ArgumentParser(description=descStr)

	parser.add_argument('--sparams', nargs=3, dest='sparams',
			required=False, help='arguments: R, r, l')

	args = parser.parse_args()

	turtle.setup(width=0.8)
	turtle.shape('turtle')
	turtle.title('Spirograph.')
	turtle.onkey(saveDrawing, 's')
	turtle.listen()
	turtle.hideturtle()

	if args.sparams:
		params = [float(x) for x in args.sparams]
		col = (0.0, 0.0, 0.0)
		spiro = Spiro(0, 0, col, *params)
		spiro.draw()
	else:
		spiroAnim = SpiroAnimator(4)
		turtle.onkey(spiroAnim.toggleTurtles, 't')
		turtle.onkey(spiroAnim.restart, 'space')

	turtle.mainloop()