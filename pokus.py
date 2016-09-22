import sys


def vector(b1,b2):
    return tuple([b2[0]-b1[0],b2[1]-b1[1]])

def isParallel(v1,v2):
    if v2[0]==0:
        if v1[0]!=0:
            return False
        else:
            if (v1[1]*v2[1])==0:
                return v1[1]==v2[1]
            else:
                return True
    if v2[1]==0:
        if v1[1]!=0:
            return False
        else:
            return v1[0]!=0
    return (v1[0]/v2[0]) == (v1[1]/v2[1])


class Line(object):
    def __init__(self, p1, p2):
        self.point = tuple(p1)
        self.svector = (p2[0] - p1[0], p2[1] - p1[1])
        if self.svector == (0,0):
            sys.exit("Problem, p1 = p2 = %s" % p1)
        self.points = set()
        self.points.add(tuple(p1))
        self.points.add(tuple(p2))
        if self.svector[0] == 0:
            self.k=0
        else:
            self.k = self.svector[1]/self.svector[0]
            if self.k == 0: # negative zero is problem for repr
                self.k = 0
        if self.k == 0 and self.svector[0] == 0:
            self.q = 0
            self.point=(p1[0],0)
            self.svector=(0,1)
            self.vertical = True
        else:
            self.q = p1[1]-self.k*p1[0]
            self.vertical = False


    def __repr__(self):
        if (self.vertical):
            return "s= ( %s , %s ), p= ( %s , %s )" % (self.svector[0], self.svector[1], self.point[0], self.point[1])
        else:
            return "y= %s * x + %s" % (self.k, self.q)


    def __eq__(self,other):
        if isinstance(other, Line):
            if self.vertical or other.vertical:
                return (self.svector == other.svector) and (self.point == other.point)
            else:
                vct = vector(self.point, other.point)
                if vct == (0, 0):
                    return True
                return isParallel(self.svector, other.svector) and isParallel(vct, self.svector)
        else:
            return False

    def __ne__(self, other):
        return (not self.__eq__(other))

    def __hash__(self):
        return hash(self.__repr__())

    def isPointYour(self,p):
        if self.vertical:
            if p[0] == self.point[0]:
                self.points.add(tuple(p))
                return True
            else:
                return False
        else:
            if self.k*p[0]+self.q == p[1]:
                self.points.add(tuple(p))
                return True
        return False


def checkio(lst):
    lines = set() #only dissimilar lines
    tlst = list(map(lambda x:tuple(x),lst))
    # lines determined by every pair of points
    for p in tlst:
        for q in tlst:
            if q!=p:
                lines.add(Line(p,q))
    # offering every point to every line
    for p in tlst:
        for l in lines:
            l.isPointYour(p)

    # filter only lines with 3 or more points...
    return len([l for l in lines if len(l.points)>2])




#checkio([[3, 3], [5, 5], [8, 8], [2, 8], [8, 2]])
# -> 2 lines

#checkio([[2, 2], [2, 5], [2, 8], [5, 2], [7, 2], [8, 2], [9, 2], [4, 5], [4, 8], [7, 5], [5, 8], [9, 8]])
# -> 6 lines