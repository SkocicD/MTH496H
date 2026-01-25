import numpy as np
import matplotlib.pyplot as plt


def dist(p1, p2):
    return ((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)**.5


def plot_point(p, ax):
    x, y = p
    ax.plot([x], [y], 'ro')


class line:
    def __init__(self, p1=None, p2=None, a=None, b=None, c=None):
        if p1 is not None and p2 is not None:
            self.p1 = p1
            self.p2 = p2

            x1, y1 = p1
            x2, y2 = p2

            self.a = y2-y1
            self.b = x1-x2
            self.c = self.a*x1+self.b*y1
            self.length = dist(self.p1, self.p2)

        if a is not None and b is not None and c is not None:
            self.a = a
            self.b = b
            self.c = c

    def perp(self, intersection):
        x, y = intersection
        a = self.b
        b = -self.a
        c = a*x+b*y

        return line(a=a, b=b, c=c)

    def midpoint(self):
        return ((self.p1[0]+self.p2[0])/2, (self.p1[1]+self.p2[1])/2)

    def intersect(self, other):
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
        intersect = (intersect[0, 0], intersect[1, 0])
        return intersect

    def has_vertex(self, v):
        return self.p1 == v or self.p2 == v

    def plot(self, ax, color='k'):
        xs, ys = list(zip(self.p1, self.p2))
        ax.plot(xs, ys, color=color)

    def __eq__(self, o):
        p1, p2 = sorted([self.p1, self.p2])
        op1, op2 = sorted([o.p1, o.p2])
        return p1 == op1 and p2 == op2

    def __hash__(self):
        p1, p2 = sorted([self.p1, self.p2])
        return hash((p2, p2))

    def __str__(self):
        return f'{self.a}x + {self.b}y = {self.c}'


class triangle:
    def __init__(self, p1, p2, p3):
        self.ps = [p1, p2, p3]
        self.edges = [line(p1, p2), line(p2, p3), line(p3, p1)]
        self.circumcenter = self.calculate_circumcenter()
        self.radius = dist(self.circumcenter, self.ps[0])
        self.r_squared = self.radius**2

    def calculate_circumcenter(self):
        midpoint1 = self.edges[0].midpoint()
        midpoint2 = self.edges[1].midpoint()
        perp1 = self.edges[0].perp(midpoint1)
        perp2 = self.edges[1].perp(midpoint2)

        return perp1.intersect(perp2)

    def in_circumcircle(self, p):
        return dist(self.circumcenter, p) < self.radius

    def plot_circumcircle(self, ax):
        c = plt.Circle(self.circumcenter, self.radius, fill=False)
        ax.add_artist(c)

    def has_vertex(self, v):
        return v in self.ps

    def is_obtuse(self):
        # make a,b,c the lengths of the edges, c longest
        a, b, c = sorted([edge.length for edge in self.edges])
        return c**2 > a**2 + b**2


def watsons(vertices):
    vertices = sorted(vertices)

    super_tri = triangle((0, 100), (100, -100), (-100, -100))
    incomplete_triangles = [super_tri]
    complete_triangles = []

    for v in vertices:
        x, y = v
        surrounding_edges = set()
        edges_to_remove = set()

        i = 0
        while i < len(incomplete_triangles):
            tri = incomplete_triangles[i]
            tx, ty = tri.circumcenter
            Dx_squared = (x - tx)**2
            if Dx_squared >= tri.r_squared:
                incomplete_triangles.remove(tri)
                complete_triangles.append(tri)
                continue

            if tri.in_circumcircle(v):
                for edge in tri.edges:
                    if edge in surrounding_edges:
                        edges_to_remove.add(edge)
                    surrounding_edges.add(edge)
                incomplete_triangles.remove(tri)
                continue
            i += 1

        # clear any edges which appeared in more than one invalid triangle
        surrounding_edges = surrounding_edges - edges_to_remove

        # make triangles with each edge and the current vertex
        for edge in surrounding_edges:
            incomplete_triangles.append(triangle(v, edge.p1, edge.p2))

    # make all imcomplete triangles complete
    complete_triangles.extend(incomplete_triangles)

    # remove any triangles that have the super vertices as a part
    i = 0
    while i < len(complete_triangles):
        tri = complete_triangles[i]
        for v in super_tri.ps:
            if tri.has_vertex(v):
                complete_triangles.remove(tri)
                break
        else:
            i += 1

    return complete_triangles


if __name__ == '__main__':
    vertices = []

    def on_click(event):
        if ax := event.inaxes:
            x, y = event.xdata, event.ydata
            vertices.append((x, y))

            tris = watsons(vertices)

            edges = set()
            for tri in tris:
                for edge in tri.edges:
                    edges.add(edge)

            ax.clear()
            ax.set_xlim(0, 10)
            ax.set_ylim(0, 10)
            ax.set_title("Click anywhere inside the axes")

            for edge in edges:
                edge.plot(ax)
            for v in vertices:
                plt.plot(v[0], v[1], 'o')
            event.canvas.draw_idle()

    fig, ax = plt.subplots()

    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_title("Click anywhere inside the axes")

    # Connect the click handler
    cid = fig.canvas.mpl_connect('button_press_event', on_click)

    plt.show()
