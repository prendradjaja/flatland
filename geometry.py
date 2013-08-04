import math
import random
from vec2d import Vec2d

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

    def update_mouse(self, event):
        self.mouse = event.x, event.y

    def blah():
        slices = 3
        for s in range(slices):
            gray = hexgray(200 + s*10)
            slice_left = left + s*(width/slices)
            slice_right = left + (s+1)*(width/slices)
            slicerect = [slice_left, top, slice_right, bottom]
            canvas.create_rectangle(*slicerect, fill=gray, width=0)

    def add_random_polygons(self, width, height, n):
        for _ in range(n):
            self.add_regular_polygon(random.randint(3, 7),
                                      random.randint(0, width),
                                      random.randint(0, height),
                                      random.randint(20, 70),
                                      random.randint(0, 360))

    def add_demo_polygons(self):
        self.add_regular_polygon(5, 22, 29, 68, 62)
        self.add_regular_polygon(6, 125, 89, 28, 332)
        self.add_regular_polygon(4, 185, 298, 63, 76)
        self.add_regular_polygon(3, 89, 160, 50, 187)

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
