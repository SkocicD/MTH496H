from voronoi_diagram import voronoi
from bowyer_watson import watsons
import matplotlib.pyplot as plt


def crust(points):
    S = points
    V, _ = voronoi(S)
    S_prime = S + V

    delaunay = watsons(S_prime)

    crust_edges = []

    for tri in delaunay:
        for edge in tri.edges:
            if edge.p1 in S and edge.p2 in S:
                crust_edges.append(edge)

    return crust_edges


if __name__ == '__main__':
    points = []

    def on_click(event):
        if ax := event.inaxes:
            x, y = event.xdata, event.ydata
            points.append((x, y))

            crust_edges = crust(points)

            ax.clear()
            ax.set_xlim(0, 10)
            ax.set_ylim(0, 10)
            ax.set_title("Click anywhere inside the axes")

            for p in points:
                plt.plot(p[0], p[1], 'ko')
            for edge in crust_edges:
                edge.plot(ax, color='r')
            event.canvas.draw_idle()

    fig, ax = plt.subplots()

    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_title("Click anywhere inside the axes")

    # Connect the click handler
    cid = fig.canvas.mpl_connect('button_press_event', on_click)

    plt.show()
