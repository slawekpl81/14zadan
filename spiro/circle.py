import math
import turtle

def drawCircleTurtle(r, x=0, y=0, color='black'):
    """
        r- promien
        x,y - srodek okregu
    """
    turtle.up()
    turtle.setpos(x+r, y)
    turtle.down()
    turtle.pencolor(color)
    
    for i in range(0, 365, 5):
        a = math.radians((i))
        turtle.setpos(x+ r*math.cos(a), y+r*math.sin(a))
        
    return 'OK'

if __name__ == '__main__':
    drawCircleTurtle(50)
    turtle.mainloop()