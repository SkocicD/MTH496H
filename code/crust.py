from voronoi_diagram import voronoi
from delaunay_triangulation import delaunay
from geometry import Point
import matplotlib.pyplot as plt


def crust(points):
    global V, tri_edges, vor_edges
    S = points
    V, vor_edges = voronoi(S)
    S_prime = S + V

    triangulation = delaunay(S_prime)

    crust_edges = []

    tri_edges = set()

    for tri in triangulation:
        for edge in tri.edges:
            tri_edges.add(edge)
            if edge.p1 in S and edge.p2 in S:
                crust_edges.append(edge)

    return crust_edges


if __name__ == '__main__':
    points = []
    crust_edges = []
    drawn = False
    step = 0

    def on_key(event):
        global step, V, tri_edges, vor_edges
        if event.key == 'enter':
            if step == 0:
                for edge in vor_edges:
                    edge.plot(ax, '#5D7DC7')
            elif step == 1:
                for v in V:
                    v.plot(ax, 'g', 'x', markersize=5)
            elif step == 2:
                ax.clear()
                ax.set_xlim(0, 10)
                ax.set_ylim(0, 10)
                for p in points:
                    p.plot(ax, markersize=5)
                for v in V:
                    v.plot(ax, 'g', 'x', markersize=5)
            elif step == 3:
                for edge in tri_edges:
                    edge.plot(ax, '#C75D5D')
            elif step == 4:
                for edge in crust_edges:
                    edge.plot(ax, color='k')
            elif step == 5:
                ax.clear()
                ax.set_xlim(0, 10)
                ax.set_ylim(0, 10)
                for p in points:
                    p.plot(ax, markersize=5)
                for edge in crust_edges:
                    edge.plot(ax, color='k')

            event.canvas.draw_idle()
            step += 1

        if event.key == 'c':
            if not drawn:
                for edge in crust_edges:
                    edge.plot(ax, color='k')
                event.canvas.draw_idle()

    def on_click(event):
        global crust_edges, step
        if ax := event.inaxes:
            x, y = event.xdata, event.ydata
            points.append(Point(x, y))

            crust_edges = crust(points)

            ax.clear()
            ax.set_xlim(0, 10)
            ax.set_ylim(0, 10)
            ax.set_title("Click anywhere inside the axes")
            step = 0

            for p in points:
                p.plot(ax, markersize=5)
            # for edge in crust_edges:
            #     edge.plot(ax, color='k')
            event.canvas.draw_idle()

    fig, ax = plt.subplots()

    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_title("Click anywhere inside the axes")

    # Connect the click handler
    cid = fig.canvas.mpl_connect('button_press_event', on_click)
    cid = fig.canvas.mpl_connect('key_press_event', on_key)

    # plt.axis('equal')
    plt.show()
