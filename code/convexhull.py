import matplotlib.pyplot as plt
from math import atan


def angle_between(p1, p2):
    ydiff = p2[1]-p1[1]
    xdiff = p2[0]-p1[0]
    # Handle division by zero
    if xdiff == 0:
        arg = (ydiff/abs(ydiff)) * float('inf')
    else:
        arg = ydiff/xdiff

    return atan(arg)


def sort_around(points, clockwise: bool):
    '''sorts the points in CW/CCW order starting with the leftmost point'''
    start = points[0]
    angles = []
    for i, p in enumerate(points[1:]):
        a = angle_between(start, p)
        angles.append((a, i+1))
    angles = sorted(angles, reverse=clockwise)
    ordered = [start]
    for a, i in angles:
        ordered.append(points[i])
    return ordered


def find_tangent(hull1, hull2, upper: bool):
    # find the rightmost point of the left hull
    # and the leftmost point of the right hull
    hull1_around = sort_around(hull1, clockwise=not upper)
    hull2_around = sort_around(hull2, clockwise=upper)

    left = hull1_around.index(hull1[-1])
    right = hull2_around.index(hull2[0])

    # walk clockwise around the right hull until the line is tangent
    # then walk counterclockwise around the left hull until the line is tangent
    # repeat until they are both tangent
    while 1:
        done = True
        while (not upper) ^ (angle_between(hull1_around[left], hull2_around[right]) < angle_between(hull1_around[left], hull2_around[(right+1) % len(hull2)])):
            right = (right+1) % len(hull2)
        while (not upper) ^ (angle_between(hull2_around[right], hull1_around[left]) > angle_between(hull2_around[right], hull1_around[(left+1) % len(hull1)])):
            left = (left+1) % len(hull1)
            done = False
        if done:
            break
    return (hull1_around[left], hull2_around[right])


def combine_halves(hull1, hull2):
    # print(hull1, hull2)
    upper_tangent = find_tangent(hull1, hull2, upper=True)
    lower_tangent = find_tangent(hull1, hull2, upper=False)
    # print(' ', upper_tangent, lower_tangent)

    left_clockwise = sort_around(hull1, clockwise=True)
    right_clockwise = sort_around(hull2, clockwise=True)
    # print('  ', left_clockwise, right_clockwise)

    hull = [lower_tangent[0]]

    index = left_clockwise.index(hull[0])
    while left_clockwise[index] != upper_tangent[0]:
        index = (index + 1) % len(hull1)
        hull.append(left_clockwise[index])

    index = right_clockwise.index(upper_tangent[1])
    hull.append(upper_tangent[1])

    while right_clockwise[index] != lower_tangent[1]:
        index = (index + 1) % len(hull2)
        hull.append(right_clockwise[index])

    # print()

    return sorted(hull)


def convexhull(points):
    '''Assumes the points are sorted by x-value'''
    L = len(points)
    if L < 4:
        return points
    L = int(L/2)
    return combine_halves(convexhull(points[:L]), convexhull(points[L:]))


if __name__ == '__main__':
    # points = [
    #     (1, 1),
    #     (2, 3),
    #     (5, 4),
    #     (4, 2),
    #     (3, -1),
    #     (7, 9),
    #     (6, 3)
    # ]
    # points = sorted(points)
    # print(convexhull(points))
    # plot_hulls([], points)

    # Create figure and axes
    fig, ax = plt.subplots()
    ax.set_title("Click to add points, press h to draw the convex hull")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)

    points = []
    # Create an empty scatter plot
    scatter = ax.scatter([], [], s=5, c='k')

    def on_click(event):
        # Ignore clicks outside the axes
        if event.inaxes != ax:
            return

        # Get click coordinates
        points.append((event.xdata, event.ydata))

        # Update scatter plot
        scatter.set_offsets(points)

        # Redraw the figure
        fig.canvas.draw_idle()

    def on_key(event):
        global points
        if event.key == 'h':
            points = sorted(points)
            hull = convexhull(points)
            hull = sort_around(hull, clockwise=True)
            hull.append(hull[0])
            x = [p[0] for p in hull]
            y = [p[1] for p in hull]
            ax.plot(x, y, c='k', linestyle='--')
            fig.canvas.draw_idle()

    fig.canvas.mpl_connect("key_press_event", on_key)
    fig.canvas.mpl_connect("button_press_event", on_click)
    plt.show()
