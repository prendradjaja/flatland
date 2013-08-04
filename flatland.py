import sys
import tkinter
import geometry
from util import Clipper
from renderer1d import Renderer1D
from renderer2d import Renderer2D

FRAME_RATE = 30
SLICES = 20

def yank_shapes(event):
    c = Clipper()
    for shape in world.shapes:
        c.add(shape.makecode)
    c.copy(verbose=True)

root = tkinter.Tk()

mycanvas = tkinter.Canvas(root, width=600, height=400, background='white')
mycanvas.pack()

world = geometry.World(mycanvas)
renderer1d = Renderer1D(world, mycanvas, SLICES)
renderer2d = Renderer2D(world, mycanvas, FRAME_RATE, renderer1d)

root.bind('<Control-Key-c>', exit)
root.bind('<Control-Key-e>', exit)
root.bind('<Control-Key-y>', yank_shapes)
root.bind('<Motion>', world.update_mouse)

world.add_regular_polygon(5, 100, 100, 50, 180)
#world.add_demo_polygons()
#world.add_random_polygons(300, 300, 4)

renderer2d.draw()
root.mainloop()
