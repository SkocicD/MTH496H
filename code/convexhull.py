import matplotlib.pyplot as plt
from geometry import Point, LineSegment
from itertools import pairwise


def slope(p1, p2):
    ydiff = p2.y-p1.y
    xdiff = p2.x-p1.x

    if xdiff == 0:
        if p1.y < p2.y:
            slope = float('inf')
        else:
            slope = -float('inf')
    else:
        slope = ydiff/xdiff

    return slope


# def sort_around(points, clockwise: bool):
#     '''sorts the points in CW/CCW order starting with the leftmost point'''
#     start = points[0]
#     angles = []
#     for i, p in enumerate(points[1:]):
#         a = angle_between(start, p)
#         angles.append((a, i+1))
#     angles = sorted(angles, reverse=clockwise)
#     ordered = [start]
#     for a, i in angles:
#         ordered.append(points[i])
#     return ordered


# def find_tangent(hull1, hull2, upper: bool):
#     # find the rightmost point of the left hull
#     # and the leftmost point of the right hull
#     hull1_around = sort_around(hull1, clockwise=not upper)
#     hull2_around = sort_around(hull2, clockwise=upper)
#
#     left = hull1_around.index(hull1[-1])
#     right = hull2_around.index(hull2[0])
#
#     # walk clockwise around the right hull until the line is tangent
#     # then walk counterclockwise around the left hull until the line is tangent
#     # repeat until they are both tangent
#     while 1:
#         done = True
#         while (not upper) ^ (angle_between(hull1_around[left], hull2_around[right]) < angle_between(hull1_around[left], hull2_around[(right+1) % len(hull2)])):
#             right = (right+1) % len(hull2)
#         while (not upper) ^ (angle_between(hull2_around[right], hull1_around[left]) > angle_between(hull2_around[right], hull1_around[(left+1) % len(hull1)])):
#             left = (left+1) % len(hull1)
#             done = False
#         if done:
#             break
#     return (hull1_around[left], hull2_around[right])
#

def find_iter_order(hull, side):
    '''
    we can start from the leftmost point of the hull
    at first, as long as we are increasing in y-value, then we are walking cw.
    Once we hit the max, we decrease until the rightmost point
    we can walk this path and keep track. Do the opposite for going ccw
    '''

    # find the highest and lowest y-values of the hull
    mx = -float('inf')
    mn = float('inf')
    mxi = mni = 0
    for i, p in enumerate(hull):
        if p.y <= mn:
            mn = p.y
            mni = i
        if p.y >= mx:
            mx = p.y
            mxi = i

    start = hull[0]
    end = hull[-1]
    top = []
    bottom = []
    for i, p in enumerate(hull):
        if i <= mxi and p.y >= start.y:
            top.append(p)
        if i <= mni and p.y <= start.y:
            bottom.append(p)
        if i > mxi and p.y >= end.y:
            top.append(p)
        if i > mni and p.y <= end.y:
            bottom.append(p)
    if side == 'left':
        top, bottom = top[::-1], bottom[::-1]

    return top, bottom


def find_tangent_point(reference_point, iter_order_list, direction):
    changed = False
    done = False
    while not done:
        done = True
        if len(iter_order_list) < 2:
            return changed
        thispoint = iter_order_list[0]
        nextpoint = iter_order_list[1]
        if direction == 'cw':
            if slope(reference_point, nextpoint) > slope(thispoint, thispoint):
                iter_order_list.pop(0)
                changed = True
                done = False
        elif direction == 'ccw':
            if slope(reference_point, nextpoint) < slope(thispoint, thispoint):
                iter_order_list.pop(0)
                changed = True
                done = False
    return changed


def combine_halves(left_hull, right_hull):
    left_top, left_bottom = find_iter_order(left_hull, 'left')
    right_top, right_bottom = find_iter_order(right_hull, 'right')

    print('combining:')
    print('left')
    for p in left_hull:
        print(p)
    print('right')
    for p in right_hull:
        print(p)

    # get the bottom tangent
    changed = True
    while changed:
        changed = False
        changed |= find_tangent_point(left_bottom[0], right_bottom, 'ccw')
        changed |= find_tangent_point(right_bottom[0], left_bottom, 'cw')

    # get the top tangent
    changed = True
    while changed:
        changed = False
        changed |= find_tangent_point(left_top[0], right_top, 'cw')
        changed |= find_tangent_point(right_top[0], left_top, 'ccw')

    new_hull = []

    print(len(left_hull), len(right_hull))
    print('left top')
    for p in left_top:
        print(p)
    print('left bottom')
    for p in left_bottom:
        print(p)
    print('right top')
    for p in right_top:
        print(p)
    print('right bottom')
    for p in right_bottom:
        print(p)
    print()

    # combine the parts of the hull that remain
    left_top = left_top[::-1]
    left_bottom = left_bottom[::-1]
    while left_bottom or left_top or right_bottom or right_top:
        next_arr = left_bottom
        if not next_arr or (left_top and left_top[0].x < next_arr[0].x):
            next_arr = left_top
        if not next_arr or (right_bottom and right_bottom[0].x < next_arr[0].x):
            next_arr = right_bottom
        if not next_arr or (right_top and right_top[0].x < next_arr[0].x):
            next_arr = right_top
        next_point = next_arr.pop(0)
        if new_hull and new_hull[-1] == next_point:
            continue
        new_hull.append(next_point)
    return new_hull


# def combine_halves2(hull1, hull2):
#     # print(hull1, hull2)
#     upper_tangent = find_tangent(hull1, hull2, upper=True)
#     lower_tangent = find_tangent(hull1, hull2, upper=False)
#     # print(' ', upper_tangent, lower_tangent)
#
#     left_clockwise = sort_around(hull1, clockwise=True)
#     right_clockwise = sort_around(hull2, clockwise=True)
#     # print('  ', left_clockwise, right_clockwise)
#
#     hull = [lower_tangent[0]]
#
#     index = left_clockwise.index(hull[0])
#     while left_clockwise[index] != upper_tangent[0]:
#         index = (index + 1) % len(hull1)
#         hull.append(left_clockwise[index])
#
#     index = right_clockwise.index(upper_tangent[1])
#     hull.append(upper_tangent[1])
#
#     while right_clockwise[index] != lower_tangent[1]:
#         index = (index + 1) % len(hull2)
#         hull.append(right_clockwise[index])
#
#     # print()
#
#     return sorted(hull)


def convexhull(points):
    '''Assumes the points are sorted by x-value'''
    L = len(points)
    if L <= 3:
        return points
    L = int(L/2)
    return combine_halves(convexhull(points[:L]), convexhull(points[L:]))


if __name__ == '__main__':

    points = []
    points.append(Point(0, 0))
    points.append(Point(1, 1))
    points.append(Point(2, -1))
    points.append(Point(3, 0))
    points.append(Point(4, 1))
    points.append(Point(5, -1))
    points.append(Point(6, 0))
    top, bottom = find_iter_order(points, 'left')
    for point in top:
        print(point)
    print()
    for point in bottom:
        print(point)

    hull = convexhull(points)
    print('hull:')
    for point in hull:
        print(point)
    print()

    top, bottom = find_iter_order(hull, 'left')
    for point in top:
        print(point)
    print()
    for point in bottom:
        print(point)

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

        ax.clear()
        ax.set_title("Click to add points, press h to draw the convex hull")
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        # Get click coordinates
        points.append(Point(event.xdata, event.ydata))
        for point in points:
            point.plot(ax)

        # Redraw the figure
        fig.canvas.draw_idle()

    def on_key(event):
        global points
        if event.key == 'h':
            points = sorted(points)
            hull = convexhull(points)
            hull.append(hull[0])
            top, bottom = find_iter_order(hull, 'right')
            for p1, p2 in pairwise(top):
                seg = LineSegment(p1, p2)
                seg.plot(ax)
            for p1, p2 in pairwise(bottom):
                seg = LineSegment(p1, p2)
                seg.plot(ax)
            fig.canvas.draw_idle()

    fig.canvas.mpl_connect("key_press_event", on_key)
    fig.canvas.mpl_connect("button_press_event", on_click)
    plt.show()
