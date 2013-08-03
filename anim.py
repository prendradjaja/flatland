import tkinter

FRAME_RATE = 30

x, y = 0, 0

def showxy(event):
    global x, y
    x, y = event.x, event.y

root = tkinter.Tk()
root.bind('<Control-Key-c>', exit)
root.bind('<Motion>', showxy)

mycanvas = tkinter.Canvas(root, width=600, height=400, background='white')
mycanvas.pack()

i = 200

def draw():
    global i
    i += 1
    mycanvas.delete('all')
    mycanvas.create_line(x, y, i, 400)
    root.after(1000//FRAME_RATE, draw)

draw()

root.mainloop()
