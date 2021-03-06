import tkinter
from renderer1d import Renderer1D

class Renderer2D:
    def __init__(self, world, canvas, frame_rate, renderer1d):
        self.world = world
        self.canvas = canvas
        self.frame_rate = frame_rate
        self.renderer1d = renderer1d

    def draw(self):
        self.canvas.delete(tkinter.ALL)
        for shape in self.world.shapes:
            self.canvas.create_polygon(shape.coords)
        self.renderer1d.draw([300, 300, 600, 400])
        self.canvas.after(1000 // self.frame_rate, self.draw)
