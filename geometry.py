import math
import tkinter
import random
from vec2d import Vec2d

def dist_to_gray(dist):
    dist = int(dist)
    if dist > 255:
        dist = 255
    #return 'black'
    return hexgray(dist)

def draw_sight_line(canvas, ray):
    x, y, angle = ray.things
    length = 500
    endx = x + length*math.sin(angle)
    endy = y + length*math.cos(angle)
    canvas.create_line(x, y, endx, endy, fill='yellow')

def hexstr(n):
    return hex(n)[2:].zfill(2)

def randcolor():
    red = random.randrange(256)
    green = random.randrange(256)
    blue = random.randrange(256)
    return '#' + hexstr(red) + hexstr(green) + hexstr(blue)

def hexgray(num):
    """num 0-255 -> hex #000000-#ffffff"""
    return '#' + hexstr(num)*3

class World:
    def __init__(self, canvas):
        """Creates the world! Should only be used once."""
        self.canvas = canvas
        self.shapes = []
        self.mouse = (0, 0)

    @property
    def observer(self):
        x, y = 200, 200
        xmouse, ymouse = self.mouse
        fov = math.pi/6
        angle = math.atan2(ymouse-y, x-xmouse) - math.pi/2
        return x, y, angle, math.pi/6

    @property
    def mouseobserver(self):
        x, y = 200, 200
        xmouse, ymouse = self.mouse
        angle = math.atan2(ymouse-y, x-xmouse) - math.pi/2
        return x, y, angle

    def add_shape(self, shape):
        self.shapes.append(shape)

    def add_regular_polygon(self, *args):
        self.shapes.append(RegularPolygon(*args))

    def draw(self, canvas, frame_rate):
        canvas.delete(tkinter.ALL)
        for shape in self.shapes:
            canvas.create_polygon(shape.coords)
        #self.draw_view(canvas, [300, 300, 600, 400], self.observer)
        self.draw_view(canvas, [300, 300, 600, 400], self.observer)
        canvas.after(1000 // frame_rate, lambda: self.draw(canvas, frame_rate))
        #make_dot(canvas, *self.mouse)

    def update_mouse(self, event):
        self.mouse = event.x, event.y

    def draw_view(self, canvas, viewrect, observer):
        """viewrect: coordinates where the viewing rectangle should be placed.
        observer: [x, y, angle, fieldofview]"""
        obsx, obsy, obsangle, obsfov = observer
        #leftray = Ray(obsx, obsy, obsangle - obsfov/2, canvas)
        #rightray = Ray(obsx, obsy, obsangle + obsfov/2, canvas)
        #draw_sight_line(canvas, leftray)
        #draw_sight_line(canvas, rightray)
        left, top, right, bottom = viewrect
        outlinerect = left-1, top-1, right, bottom
        width = right - left
        canvas.create_rectangle(*viewrect)
        slices = 30
        slicewidth = width/(slices+1)
        for x in range(0, slices+1):
            ray = Ray(obsx, obsy, obsangle + obsfov/2 - x*obsfov/slices, canvas)
            draw_sight_line(canvas, ray)
            gray = self.ray_trace(ray)
            canvas.create_rectangle(left + x*slicewidth, top, left + (x+1)*slicewidth, bottom, fill=gray, width=0)
#        slicewidth = 1
#        for x in range(left, right, slicewidth):
#            canvas.create_rectangle(x, top, x+slicewidth, bottom, fill=randcolor(), width=0)

    def draw_mouse_view(self, canvas, viewrect, observer):
        """viewrect: coordinates where the viewing rectangle should be placed.
        observer: [x, y, angle, fieldofview]"""
        obsx, obsy, obsangle = observer
        ray = Ray(obsx, obsy, obsangle, canvas)
        draw_sight_line(canvas, ray)
        left, top, right, bottom = viewrect
        outlinerect = left-1, top-1, right, bottom
        width = right - left
        canvas.create_rectangle(*viewrect, fill=self.ray_trace(ray))

    def ray_trace(self, ray):
        """Return the appropriate shade of grey"""
        closest_intersection = None
        for shape in self.shapes:
            intersection = shape.intersects_ray(self.canvas, ray)
            if intersection:
                #print(shape)
                if closest_intersection is None:
                    closest_intersection, closest_distance = intersection
                elif intersection[1] < closest_distance:
                    closest_intersection, closest_distance = intersection
        if closest_intersection:
            make_dot(self.canvas, closest_intersection)
            return dist_to_gray(closest_distance)

    def blah():
        slices = 3
        for s in range(slices):
            gray = hexgray(200 + s*10)
            slice_left = left + s*(width/slices)
            slice_right = left + (s+1)*(width/slices)
            slicerect = [slice_left, top, slice_right, bottom]
            canvas.create_rectangle(*slicerect, fill=gray, width=0)

class RegularPolygon:
    names = [None, None, None,
             'triangle',
             'square',
             'pentagon',
             'hexagon',
             'heptagon',
             'octagon',
             'nonagon',
             'decagon']

    def __init__(self, n, x, y, r, a):
        """Creates a regular polygon at angle A (degrees) with N sides
        centered at (X, Y) such that a circumscribing circle has radius R."""
        self.sides = n
        self.x = x
        self.y = y
        self.radius = r
        self.angle = a

    def __repr__(self):
        return 'RegularPolygon({0})'.format(self.args)

    @property
    def makecode(self):
        return 'world.add_regular_polygon({0})'.format(self.args)

    @property
    def args(self):
        return '{n}, {x}, {y}, {r}, {a}'.format(n = self.sides,
                                                x = self.x,
                                                y = self.y,
                                                r = self.radius,
                                                a = self.angle)

    @property
    def coords(self):
        coords = []
        angle = 2*math.pi/self.sides
        for i in range(self.sides):
            x = self.x + self.radius*math.sin(i*angle +
            math.radians(self.angle))
            y = self.y + self.radius*math.cos(i*angle +
            math.radians(self.angle))
            coords.extend([x, y])
        return coords

    def intersects_ray(self, canvas, ray):
        """Checks if any side of the polygon intersects RAY.
        Returns the the nearest intersection and distance if so.
        Returns None otherwise.
        Implements this algorithm:
        http://stackoverflow.com/questions/563198/how-do-you-detect-where-two-line-segments-intersect
        """
        coords = self.coords
        points = []
        for i in range(len(coords)//2):
            points.append((coords[2*i], coords[2*i+1]))
        closest_intersection = None
        closest_distance = 0
        for i in range(len(points)):
            ax, ay = points[i-1]
            bx, by = points[i]
            #make_dot(canvas, ax, ay)
            #make_dot(canvas, bx, by)
            intersection = ray.intersects_side(ax, ay, bx, by)
            if intersection:
                if closest_intersection is None:
                    closest_intersection = intersection[0]
                    closest_distance = intersection[1]
                elif intersection[1] < closest_distance:
                    closest_intersection = intersection[0]
                    closest_distance = intersection[1]
        if closest_intersection:
            return closest_intersection, closest_distance

class Ray:
    def __init__(self, x, y, angle, canvas):
        self.x = x
        self.y = y
        self.angle = angle
        self.canvas = canvas

    @property
    def things(self):
        return self.x, self.y, self.angle

    def intersects_side(self, ax, ay, bx, by):
        VIEWLENGTH = 1
        p = Vec2d(ax, ay)
        r = Vec2d(bx-ax, by-ay)
        q = Vec2d(self.x, self.y)
        s = Vec2d(VIEWLENGTH*math.sin(self.angle),
                  VIEWLENGTH*math.cos(self.angle))
        #make_dot(self.canvas, p)
        #make_dot(self.canvas, q)
        #make_dot(self.canvas, r)
        #make_dot(self.canvas, s)
        # note: division by zero if parallel: r x s = 0
        denom = Vec2d.cross(r, s)
        if denom == 0:
            return None
        t = Vec2d.cross((q - p), s) / denom
        u = Vec2d.cross((q - p), r) / denom
        if u < 0:
            return None
        if 0 < t < 1:
            result = p + t*r
            return result, u

def make_dot(canvas, x_or_vector, y=None):
    rad = 6
    if y is None:
        y = x_or_vector.y
        x = x_or_vector.x
    else:
        x = x_or_vector
    canvas.create_oval(x-rad/2, y-rad/2,
                       x+rad/2, y+rad/2, fill='red', width=0)
