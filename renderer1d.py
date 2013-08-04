from vec2d import Vec2d
import math

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


class Renderer1D:
    def __init__(self, world, canvas, slices):
        self.world = world
        self.canvas = canvas
        self.slices = slices

    def draw(self, viewrect):
        """viewrect: coordinates where the viewing rectangle should be placed.
        observer: [x, y, angle, fieldofview]"""
        obsx, obsy, obsangle, obsfov = self.world.observer
        #leftray = Ray(obsx, obsy, obsangle - obsfov/2, self.canvas)
        #rightray = Ray(obsx, obsy, obsangle + obsfov/2, self.canvas)
        #draw_sight_line(self.canvas, leftray)
        #draw_sight_line(self.canvas, rightray)
        left, top, right, bottom = viewrect
        outlinerect = left-1, top-1, right, bottom
        width = right - left
        self.canvas.create_rectangle(*viewrect)
        slices = self.slices
        slicewidth = width/(slices)
        for x in range(0, slices):
            ray = Ray(obsx, obsy, obsangle + obsfov/2 - x*obsfov/(slices-1), self.canvas)
            draw_sight_line(self.canvas, ray)
            gray = self.ray_trace(ray)
            self.canvas.create_rectangle(left + x*slicewidth, top, left + (x+1)*slicewidth, bottom, fill=gray, width=0)
#        slicewidth = 1
#        for x in range(left, right, slicewidth):
#            self.canvas.create_rectangle(x, top, x+slicewidth, bottom, fill=randcolor(), width=0)


    def ray_trace(self, ray):
        """Return the appropriate shade of grey"""
        closest_intersection = None
        for shape in self.world.shapes:
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

#    def draw_mouse_view(self, self.canvas, viewrect, observer):
#        """viewrect: coordinates where the viewing rectangle should be placed.
#        observer: [x, y, angle, fieldofview]"""
#        obsx, obsy, obsangle = observer
#        ray = Ray(obsx, obsy, obsangle, self.canvas)
#        draw_sight_line(self.canvas, ray)
#        left, top, right, bottom = viewrect
#        outlinerect = left-1, top-1, right, bottom
#        width = right - left
#        self.canvas.create_rectangle(*viewrect, fill=self.ray_trace(ray))

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
