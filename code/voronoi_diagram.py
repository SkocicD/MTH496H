from delaunay_triangulation import delaunay
from geometry import LineSegment, Point
import matplotlib.pyplot as plt


def voronoi(vertices):
    triangulation = delaunay(vertices)

    voronoi_edges = []
    voronoi_vertices = []
    edge_triangle_map = {}

    for tri in triangulation:
        voronoi_vertices.append(tri.circumcenter)
        # edge_triangle_map stores the triangle or triangles
        # adjacent to each edge in the delaunay triangulation
        for edge in tri.edges:
            if edge not in edge_triangle_map:
                edge_triangle_map[edge] = []
            edge_triangle_map[edge].append(tri)

    for edge in edge_triangle_map:
        if len(edge_triangle_map[edge]) == 2:
            # if this edge borders 2 triangles,
            # connect the voronoi vertices across it
            tri1 = edge_triangle_map[edge][0]
            tri2 = edge_triangle_map[edge][1]
            tri1_center = tri1.circumcenter
            tri2_center = tri2.circumcenter
            voronoi_edges.append(LineSegment(tri1_center, tri2_center))
        elif len(edge_triangle_map[edge]) == 1:
            # If there is only one triangle next to this edge
            # then it is on the border, so draw a voronoi 'ray'
            tri = edge_triangle_map[edge][0]
            voronoi_vert = tri.circumcenter
            dx = edge.midpoint.x - voronoi_vert.x
            dy = edge.midpoint.y - voronoi_vert.y

            # find the point in the triangle that is not an
            # endpoint of the current edge
            vs = tri.vertices.copy()
            vs.remove(edge.p1)
            vs.remove(edge.p2)
            third_point = vs[0]

            # If the voronoi vertex and the third triangle point
            # are on the same side of the edge, draw the line
            # from the voronoi vertex to the edge and vice versa
            tx, ty = (third_point.x, third_point.y)
            vx, vy = (voronoi_vert.x, voronoi_vert.y)
            a, b, c = edge.a, edge.b, edge.c
            side1 = a*tx + b*ty > c
            side2 = a*vx + b*vy > c
            dir = 1 if side1 == side2 else -1

            # Create a point far in the direction to
            # look like the line goes forever
            far_point = (vx + 1000*dx*dir, vy + 1000*dy*dir)
            voronoi_edges.append(LineSegment(voronoi_vert, far_point))

    return voronoi_vertices, voronoi_edges


if __name__ == '__main__':
    points = []

    def on_click(event):
        if ax := event.inaxes:
            x, y = event.xdata, event.ydata
            points.append(Point(x, y))

            voronoi_vertices, voronoi_edges = voronoi(points)

            ax.clear()
            ax.set_xlim(0, 10)
            ax.set_ylim(0, 10)
            ax.set_title("Click anywhere inside the axes")

            for p in points:
                p.plot(ax)
            for edge in voronoi_edges:
                edge.plot(ax, color='r')
            event.canvas.draw_idle()

    fig, ax = plt.subplots()

    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_title("Click anywhere inside the axes")

    # Connect the click handler
    cid = fig.canvas.mpl_connect('button_press_event', on_click)

    plt.show()
