import sys
import tkinter
import geometry
from util import Clipper

FRAME_RATE = 30

def yank_shapes(event):
    c = Clipper()
    for shape in world.shapes:
        c.add(shape.makecode)
    c.copy(verbose=True)

root = tkinter.Tk()
root.bind('<Control-Key-c>', exit)
root.bind('<Control-Key-e>', exit)
root.bind('<Control-Key-y>', yank_shapes)

mycanvas = tkinter.Canvas(root, width=600, height=400, background='white')
mycanvas.pack()

world = geometry.World(mycanvas)

root.bind('<Motion>', world.update_mouse)

import random
def add_random_polygons(world, width, height, n):
    for _ in range(n):
        world.add_regular_polygon(random.randint(3, 7),
                                  random.randint(0, width),
                                  random.randint(0, height),
                                  random.randint(20, 70),
                                  random.randint(0, 360))

def add_demo_polygons(world):
    world.add_regular_polygon(5, 22, 29, 68, 62)
    world.add_regular_polygon(6, 125, 89, 28, 332)
    world.add_regular_polygon(4, 185, 298, 63, 76)
    world.add_regular_polygon(3, 89, 160, 50, 187)

#world.add_regular_polygon(5, 100, 100, 50, 180)

add_demo_polygons(world)

#add_random_polygons(world, 300, 300, 4)

world.draw(mycanvas, FRAME_RATE)
root.mainloop()
