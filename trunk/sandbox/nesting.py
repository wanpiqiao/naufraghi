#!/usr/bin/python

import math

TOLLERANCE = 1e-4

class P:
    def __init__(self, x, y):
        self.x, self.y = x, y
    def __repr__(self):
        return "P(%f,%f)" % (self.x, self.y)
        
def dist(p1, p2):
    return math.sqrt((p1.x-p2.x)**2 + (p1.y-p2.y)**2)
    
def area(poly):
    """
    Compute polygon area using the trapezioid method
    >>> poly1 = [P(0,0),P(1,0),P(2,1),P(0,1),P(0,0)]
    >>> area(poly1)
    1.5
    >>> area(list(reversed(poly1)))
    1.5
    >>> poly2a = [P(0,0),P(1,0),P(1,1),P(2,1),P(2,2),P(1,2),P(1,1),P(0,1),P(0,0)]
    >>> area(poly2a)
    2.0
    >>> poly2b = [P(0,0),P(1,0),P(1,2),P(2,2),P(2,1),P(0,1),P(0,0)]
    >>> area(poly2b)
    0.0
    """
    a = 0.0
    for i in range(len(poly)-1):
        a += (poly[i].y + poly[i+1].y) * (poly[i].x - poly[i+1].x)
    return abs(a / 2)


def isInner(p1, poly):
    """
    Evaluate the area of all possible polygons by inserting
    the point p1 in the given poly.
    If the resulting polygon area is more than the original
    area the point is outside.
    Returns 1 if p1 is inside poly
           -1 if p1 is outside poly
            0 if p1 is on the border
    >>> poly1 = [P(0,0),P(1,0),P(2,1),P(0,1),P(0,0)]
    >>> isInner(P(2,2), poly1)
    -1
    >>> isInner(P(0.5,0.5), poly1)
    1
    >>> isInner(P(2,1), poly1)
    0
    >>> isInner(P(1,1), poly1)
    0
    """
    for i in range(len(poly)-1):
        newpoly = list(poly)    
        newpoly.insert(i+1, p1)
        res = acmp(area(poly), area(newpoly))
        if res != 1:
            return res
    return 1
    
def acmp(val1, val2, tol=TOLLERANCE):
    """
    Approximated cmp
    Returns 0 if values distance is less then `tol`
    else    cmp(val1, val2)
    
    >>> val1, val2 = 0.001, 0.002
    >>> acmp(val1, val2, tol=0.01)
    0
    >>> acmp(val1, val2, tol=0.0001) == cmp(val1, val2)
    True
    >>> acmp(val2, val1, tol=0.0001) == cmp(val2, val1)
    True
    """
    if abs(val1 - val2) < tol:
        return 0
    return cmp(val1, val2)
    

def doIntersect(seg1, seg2):
    """
    Evaluate the intersection point of two segments exixts.
    Returns True if intesects
            False if does not intesect

    >>> doIntersect([P(0,0), P(1,1)], [P(0,1), P(1,0)]) # cross
    True
    >>> doIntersect([P(0,0), P(1,1)], [P(0,0), P(1,1)]) # coincident
    True
    >>> doIntersect([P(0,0), P(1,1)], [P(0,1), P(1,2)]) # parallel
    False
    >>> doIntersect([P(0,0), P(1,1)], [P(1,1), P(1,0)]) # endpoint
    True
    >>> doIntersect([P(0,0), P(2,2)], [P(1,1), P(3,3)]) # partially coincident
    True
    >>> doIntersect([P(0,0), P(1,1)], [P(2,2), P(2,0)]) # none
    False
    """
    (p1, p2), (p3, p4) = seg1, seg2
    num1 = (p4.x - p3.x) * (p1.y - p3.y) - (p4.y - p3.y) * (p1.x - p3.x)
    num2 = (p2.x - p1.x) * (p1.y - p3.y) - (p2.y - p1.y) * (p1.x - p3.x)
    den = (p4.y - p3.y) * (p2.x - p1.x) - (p4.x - p3.x) * (p2.y - p1.y)
    if acmp(den, 0) == 0:
        if acmp(num1, 0) == 0 and acmp(num2, 0) == 0:
            return True # segments are coincident
        else:
            return False # segments are parallel
    else:
        ua = num1/den
        ub = num2/den
        if ua < 0 or ua > 1 or ub < 0 or ub > 1:
            return False
        else:
            return True


def isOver(poly1, poly2):
    """
    Returns 1 if poly1 overlaps poly1
           -1 if poly2 is not over poly2
            0 if poly1 and poly2 have a common vertex
    >>> poly1 = [P(0,0),P(1,0),P(2,1),P(0,1),P(0,0)]
    >>> poly2a = [P(0.5,0.5),P(1,2),P(2,2),P(0.5,0.5)]
    >>> isOver(poly1, poly2a)
    1
    >>> poly2b = [P(3,1),P(1,2),P(2,2),P(3,1)]
    >>> isOver(poly1, poly2b)
    -1
    >>> poly2c = [P(2,1),P(1,2),P(2,2),P(2,1)]
    >>> isOver(poly1, poly2c)
    0
    >>> poly2d = [P(1,1),P(2,0),P(2,1),P(1,1)]
    >>> isOver(poly1, poly2d)
    1
    ####### una croce non funziona!! #######
            p1 +++++
               +   +
        p2 +++++++++++++
           +           +
           +++++++++++++
               +   +
               +++++
    """
    for p1 in poly1:
        overlap = isInner(p1, poly2)
        if overlap != -1:
            return overlap
    for p2 in poly2:
        overlap = isInner(p2, poly1)
        if overlap != -1:
            return overlap
    return -1