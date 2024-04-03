from collections import namedtuple
import math
import numpy as np

Point = namedtuple("Point", ['x', 'y'])
Field = namedtuple("Field", ['h', 'w', 'o_x', 'o_y'])

VSSS = Field(1.3, 1.5, 0, 0)


def angle_between(p1, p2):
    y = p2.y - p1.y
    x = p2.x - p1.x
    ang = math.atan2(y, x)

    return ang


def reduce_angle(ang):
    while ang > math.pi:
        ang -= 2 * math.pi
    while ang < -math.pi:
        ang += 2 * math.pi
    return ang


def norm(x, y=None):
    if y is None:
        y = x.y
        x = x.x
    return math.sqrt(x ** 2 + y ** 2)


def dist(p1x, p1y, p2x=None, p2y=None):
    if p2x is None:
        p2y = p1y.y
        p2x = p1y.x
        p1y = p1x.y
        p1x = p1x.x

    return math.sqrt((p1x - p2x) ** 2 + (p1y - p2y) ** 2)


def line_circle_intersection(a, b, c, circle_center, circle_radius):
    return circle_radius > abs(a*circle_center.x + b*circle_center.y + c) / math.sqrt(a**2 + b**2)


def unit_vector(vector):
    """ Returns the unit vector of the vector."""
    if np.linalg.norm(vector) == 0:
        return np.array([0, 0])
    return vector / np.linalg.norm(vector)


def rotate_via_numpy(xy, radians):
    """Use numpy to build a rotation matrix and take the dot product."""
    x, y = xy
    c, s = np.cos(radians), np.sin(radians)
    j = np.matrix([[c, s], [-s, c]])
    m = np.dot(j, [x, y])

    return float(m.T[0]), float(m.T[1])
