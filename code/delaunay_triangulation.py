import matplotlib.pyplot as plt
from geometry import Triangle, LineSegment, Point


def delaunay(vertices):
    vertices = sorted(vertices)

    super_tri = Triangle((0, 100), (100, -100), (-100, -100))
    incomplete_triangles = [super_tri]
    complete_triangles = []

    for v in vertices:
        surrounding_edges = set()
        edges_to_remove = set()

        i = 0
        while i < len(incomplete_triangles):
            tri = incomplete_triangles[i]
            c = tri.circumcenter
            Dx_squared = (v.x - c.x)**2
            if Dx_squared >= tri.radius**2:
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
            incomplete_triangles.append(Triangle(v, edge.p1, edge.p2))

    # make all imcomplete triangles complete
    complete_triangles.extend(incomplete_triangles)

    # remove any triangles that have the super vertices as a part
    i = 0
    while i < len(complete_triangles):
        tri = complete_triangles[i]
        for v in super_tri.vertices:
            if tri.has_vertex(v):
                complete_triangles.remove(tri)
                break
        else:
            i += 1

    return complete_triangles


if __name__ == '__main__':
    points = []

    def on_click(event):
        if ax := event.inaxes:
            x, y = event.xdata, event.ydata
            points.append(Point(x, y))

            tris = delaunay(points)

            edges = set()
            for tri in tris:
                for edge in tri.edges:
                    edges.add(edge)
                tri.circumcenter.plot(ax)

            ax.clear()
            ax.set_xlim(0, 10)
            ax.set_ylim(0, 10)
            ax.set_title("Click anywhere inside the axes")

            for edge in edges:
                edge.plot(ax)
            for p in points:
                p.plot(ax)
            event.canvas.draw_idle()

    fig, ax = plt.subplots()

    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_title("Click anywhere inside the axes")

    # Connect the click handler
    cid = fig.canvas.mpl_connect('button_press_event', on_click)

    plt.show()
