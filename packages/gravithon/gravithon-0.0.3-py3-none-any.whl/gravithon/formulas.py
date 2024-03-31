import gravithon.constants.astrophisics
from Body import *
from math import pow
from numpy import ndarray
from multipledispatch import dispatch


@dispatch(float, float, float)
def gravity(m1: float, m2: float, r: float):
    return (gravithon.constants.astrophisics.G * m1 * m2) / pow(r, 2)


@dispatch(Body, Body)
def gravity(b1, b2):
    return gravity(b1.mass, b2.mass, distance(b1, b2))


@dispatch(ndarray, ndarray)
def distance(p1, p2):
    return p1 - p2


@dispatch(Body, Body)
def distance(b1, b2):
    return distance(b1.position, b2.position)
