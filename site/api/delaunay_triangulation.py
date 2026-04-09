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


def delaunay_api(points):
    p_objs = []
    for p in points:
        p_objs.append(Point(p['x'], p['y']))

    triangles = delaunay(p_objs)
    edges = set()
    for tri in triangles:
        for edge in tri.edges:
            edges.add(edge)

    edge_json_list = []
    for edge in edges:
        p1, p2 = edge.p1, edge.p2
        edge_json_list.append(
            {
                'p1': {'x': p1.x, 'y': p1.y},
                'p2': {'x': p2.x, 'y': p2.y}
            }
        )
    return {'segments': edge_json_list}


if __name__ == '__main__':
    points = []
    tris = None
    drawn = False

    def on_key(event):
        global edges, drawn, points
        if event.key == 'd':
            if not drawn:
                for edge in edges:
                    edge.plot(ax)
                event.canvas.draw_idle()
            drawn = True
        if event.key == 'x':
            print('here')
            ax.clear()
            ax.set_xlim(0, 10)
            ax.set_ylim(0, 10)
            ax.set_title("Click anywhere inside the axes")
            for p in points:
                p.plot(ax)
            event.canvas.draw_idle()
            drawn = False

    def on_click(event):
        global edges, drawn, points
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

            for p in points:
                p.plot(ax)
            event.canvas.draw_idle()
            drawn = False

    fig, ax = plt.subplots()

    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_title("Click anywhere inside the axes")

    # Connect the click handler
    cid = fig.canvas.mpl_connect('button_press_event', on_click)
    cid = fig.canvas.mpl_connect('key_press_event', on_key)

    plt.show()
