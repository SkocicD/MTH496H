from bowyer_watson import watsons, line
import matplotlib.pyplot as plt


def voronoi(vertices):
    delaunay = watsons(vertices)

    voronoi_edges = []
    voronoi_vertices = []
    edge_triangle_map = {}

    for tri in delaunay:
        voronoi_vertices.append(tri.circumcenter)
        for edge in tri.edges:
            if edge not in edge_triangle_map:
                edge_triangle_map[edge] = []
            edge_triangle_map[edge].append(tri)

    for edge in edge_triangle_map:
        # if this edge borders 2 triangles, connect voronoi edges
        if len(edge_triangle_map[edge]) > 1:
            tri1 = edge_triangle_map[edge][0]
            tri2 = edge_triangle_map[edge][1]
            tri1_center = tri1.circumcenter
            tri2_center = tri2.circumcenter
            voronoi_edges.append(line(tri1_center, tri2_center))
        else:
            tri = edge_triangle_map[edge][0]
            voronoi_vert = tri.circumcenter
            midpoint = edge.midpoint()
            dx = midpoint[0] - voronoi_vert[0]
            dy = midpoint[1] - voronoi_vert[1]

            # find the point in the triangle not in the edge
            vs = tri.ps.copy()
            vs.remove(edge.p1)
            vs.remove(edge.p2)
            third_point = vs[0]

            # If the voronoi vertex and the third triangle point
            # are on the same side of the edge, draw the line
            # from the voronoi vertex to the edge and vice versa
            tx, ty = third_point
            vx, vy = voronoi_vert
            a, b, c = edge.a, edge.b, edge.c
            side1 = a*tx + b*ty > c
            side2 = a*vx + b*vy > c
            dir = 1 if side1 == side2 else -1

            # Create a point far in the direction to
            # look like the line goes forever
            far_point = (vx + 100*dx*dir, vy + 100*dy*dir)
            voronoi_edges.append(line(voronoi_vert, far_point))

    return voronoi_vertices, voronoi_edges


if __name__ == '__main__':
    vertices = []

    def on_click(event):
        if ax := event.inaxes:
            x, y = event.xdata, event.ydata
            vertices.append((x, y))

            voronoi_vertices, voronoi_edges = voronoi(vertices)

            ax.clear()
            ax.set_xlim(0, 10)
            ax.set_ylim(0, 10)
            ax.set_title("Click anywhere inside the axes")

            for v in vertices:
                plt.plot(v[0], v[1], 'ko')
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
