import numpy as np


def handle_point_type(function_name, point):
    'Convert point into Point object if it is of type list or tuple '
    'if it is something else, raise a TypeError'

    if isinstance(point, tuple) or isinstance(point, list):
        point = Point(*point)

    if not isinstance(point, Point):
        raise TypeError(f'{function_name} must have argument(s) '
                        'of type tuple, list, or Point')
    return point


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def dist(self, other):
        return ((self.x-other.x)**2+(self.y-other.y)**2)**.5

    def plot(self, ax):
        ax.plot([self.x], [self.y], 'ko')

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __lt__(self, other):
        return (self.x, self.y) < (other.x, other.y)

    def __str__(self):
        return f'({self.x}, {self.y})'


class LineSegment:
    def __init__(self, p1: Point, p2=Point):
        p1 = handle_point_type('LineSegment', p1)
        p2 = handle_point_type('LineSegment', p2)

        self.p1 = p1
        self.p2 = p2

        self.a = p2.y-p1.y
        self.b = p1.x-p2.x
        self.c = self.a*p1.x+self.b*p1.y

        self.length = p1.dist(p2)
        self.midpoint = Point((p1.x+p2.x)/2, (p1.y+p2.y)/2)

    def perp(self, through_point):
        'return a new line object that is perpendicular'
        'to the current line through the point passed in'
        through_point = handle_point_type('perp', through_point)

        # Find another point one unit of slope further along the line
        other_point = Point(through_point.x + self.a, through_point.y + self.b)
        return LineSegment(through_point, other_point)

    def perp_bisector(self):
        return self.perp(self.midpoint)

    def intersect(self, other):
        'Computes the intersection between two line segment objects'
        'returns the intersection as if the segments were infinitely long'
        a1 = self.a
        a2 = self.b
        a3 = other.a
        a4 = other.b
        A = np.array(
            [
                [a1, a2],
                [a3, a4]
            ]
        )

        b1 = self.c
        b2 = other.c
        b = np.array(
            [
                [b1],
                [b2]
            ]
        )

        inv = np.linalg.inv(A)
        intersect = np.matmul(inv, b)
        intersect = Point(intersect[0, 0], intersect[1, 0])
        return intersect

    def has_endpoint(self, endpoint):
        'Returns True if either endpoint is the endpoint passed in'
        endpoint = handle_point_type('has_endpoint', endpoint)
        return self.p1 == endpoint or self.p2 == endpoint

    def plot(self, ax, color='k'):
        xs = [self.p1.x, self.p2.x]
        ys = [self.p1.y, self.p2.y]
        ax.plot(xs, ys, color=color)

    def __eq__(self, other):
        p1, p2 = sorted([self.p1, self.p2])
        op1, op2 = sorted([other.p1, other.p2])
        return p1 == op1 and p2 == op2

    def __hash__(self):
        p1, p2 = sorted([self.p1, self.p2])
        return hash((p2, p2))

    def __str__(self):
        return f'{self.a}x + {self.b}y = {self.c}'


class Triangle:
    def __init__(self, p1, p2, p3):
        p1 = handle_point_type('Triangle', p1)
        p2 = handle_point_type('Triangle', p2)
        p3 = handle_point_type('Triangle', p3)

        self.vertices = [p1, p2, p3]
        self.edges = [
            LineSegment(p1, p2),
            LineSegment(p2, p3),
            LineSegment(p3, p1)
        ]

        bisector1 = self.edges[0].perp_bisector()
        bisector2 = self.edges[1].perp_bisector()
        self.circumcenter = bisector1.intersect(bisector2)

        self.radius = self.circumcenter.dist(p1)

    def in_circumcircle(self, point):
        'return true if the point is in the circumcircle, false otherwise'

        point = handle_point_type('in_circumcircle', point)
        return self.circumcenter.dist(point) < self.radius

    def has_vertex(self, vertex):
        'Return true if vertex is one of the triangles vertices'

        vertex = handle_point_type('has_vertex', vertex)
        return vertex in self.vertices
