import matplotlib.pyplot as plt
from delaunay_triangulation import delaunay
from voronoi_diagram import voronoi
from geometry import Point

if __name__ == '__main__':
    points = []
    tris = None
    vor_drawn = False
    tri_drawn = False

    def on_key(event):
        global vor_edges, tri_edges, vor_drawn, tri_drawn, points
        if event.key == 'd':
            if not tri_drawn:
                for edge in tri_edges:
                    edge.plot(ax, '#C75D5D')
                event.canvas.draw_idle()
            tri_drawn = True
        if event.key == 'v':
            if not vor_drawn:
                for edge in vor_edges:
                    edge.plot(ax, '#5D7DC7')
                event.canvas.draw_idle()
            vor_drawn = True
        if event.key == 'x':
            ax.clear()
            ax.set_xlim(0, 10)
            ax.set_ylim(0, 10)
            ax.set_title("Click anywhere inside the axes")
            for p in points:
                p.plot(ax)
            event.canvas.draw_idle()
            vor_drawn = False
            tri_drawn = False

    def on_click(event):
        global vor_edges, tri_edges, vor_drawn, tri_drawn, points
        if ax := event.inaxes:
            x, y = event.xdata, event.ydata
            points.append(Point(x, y))

            tris = delaunay(points)

            _, vor_edges = voronoi(points)

            tri_edges = set()
            for tri in tris:
                for edge in tri.edges:
                    tri_edges.add(edge)
                tri.circumcenter.plot(ax)

            ax.clear()
            ax.set_xlim(0, 10)
            ax.set_ylim(0, 10)
            ax.set_title("Click anywhere inside the axes")

            vor_drawn = False
            tri_drawn = False

            for p in points:
                p.plot(ax)
            event.canvas.draw_idle()

    fig, ax = plt.subplots()

    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_title("Click anywhere inside the axes")

    # Connect the click handler
    cid = fig.canvas.mpl_connect('button_press_event', on_click)
    cid = fig.canvas.mpl_connect('key_press_event', on_key)

    plt.show()
