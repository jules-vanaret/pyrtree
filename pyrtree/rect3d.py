import math

class Rect3D(object):
    """
    A rectangle class that stores: an axis aligned rectangle, and: two
     flags (swapped_x and swapped_y).  (The flags are stored
     implicitly via swaps in the order of minx/y and maxx/y.)
    """

    __slots__ = ("x","y","z","xx","yy","zz", "swapped_x", "swapped_y", "swapped_z")

    def __init__(self, minx,miny,minz,maxx,maxy,maxz):
        self.swapped_x = (maxx < minx)
        self.swapped_y = (maxy < miny)
        self.swapped_z = (maxz < minz)
        self.x = minx
        self.y = miny
        self.z = minz
        self.xx = maxx
        self.yy = maxy
        self.zz = maxz

        if self.swapped_x: self.x,self.xx = maxx,minx
        if self.swapped_y: self.y,self.yy = maxy,miny
        if self.swapped_z: self.z,self.zz = maxz,minz

    def coords(self):
        return self.x,self.y,self.z,self.xx,self.yy,self.zz


    def overlap(self, orect):
        return self.intersect(orect).area()

    def write_raw_coords(self, toarray, idx):
        toarray[idx] = self.x
        toarray[idx+1] = self.y
        toarray[idx+2] = self.z
        toarray[idx+3] = self.xx
        toarray[idx+4] = self.yy
        toarray[idx+5] = self.zz
        if (self.swapped_x):
            toarray[idx] = self.xx
            toarray[idx+3] = self.x
        if (self.swapped_y):
            toarray[idx + 1] = self.yy
            toarray[idx + 4] = self.y
        if (self.swapped_z):
            toarray[idx + 2] = self.zz
            toarray[idx + 5] = self.z


    def area(self):
        w = self.xx - self.x
        h = self.yy - self.y
        d = self.zz - self.z
        return w * h * d

    def extent(self):
        x = self.x
        y = self.y
        z = self.z
        return (x,y,z,self.xx-x,self.yy-y,self.zz-z)

    def grow(self, amt):
        a = amt * 0.5
        return Rect3D(self.x-a,self.y-a,self.z-a,self.xx+a,self.yy+a,self.zz+a)

    def intersect(self,o):
        if self is NullRect: return NullRect
        if o is NullRect: return NullRect

        nx,ny,nz = max(self.x,o.x),max(self.y,o.y),max(self.z,o.z)
        nx2,ny2,nz2 = min(self.xx,o.xx),min(self.yy,o.yy),min(self.zz,o.zz)
        w,h,d = nx2-nx, ny2-ny, nz2-nz

        if w <= 0 or h <= 0 or d <= 0: return NullRect

        return Rect3D(nx,ny,nz,nx2,ny2,nz2)


    def does_contain(self,o):
        return self.does_containpoint( (o.x,o.y,o.z) ) and self.does_containpoint( (o.xx,o.yy,o.zz) )

    def does_intersect(self,o):
        return (self.intersect(o).area() > 0)

    def does_containpoint(self,p):
        x,y,z = p
        return (x >= self.x and x <= self.xx and y >= self.y and y <= self.yy and z >= self.z and z <= self.zz)

    def union(self,o):
        if o is NullRect: return Rect3D(self.x,self.y,self.z,self.xx,self.yy,self.zz)
        if self is NullRect: return Rect3D(o.x,o.y,o.z,o.xx,o.yy,o.zz)
        
        x = self.x
        y = self.y
        z = self.z
        xx = self.xx
        yy = self.yy
        zz = self.zz
        ox = o.x
        oy = o.y
        oz = o.z
        oxx = o.xx
        oyy = o.yy
        ozz = o.zz

        nx = x if x < ox else ox
        ny = y if y < oy else oy
        nz = z if z < oz else oz
        nx2 = xx if xx > oxx else oxx
        ny2 = yy if yy > oyy else oyy
        nz2 = zz if zz > ozz else ozz

        res = Rect3D(nx,ny,nz,nx2,ny2,nz2)

        return res
        
    def union_point(self,o):
        x,y,z = o
        return self.union(Rect3D(x,y,z,x,y,z))

    def diagonal_sq(self):
        if self is NullRect: return 0
        w = self.xx - self.x
        h = self.yy - self.y
        d = self.zz - self.z
        return w*w + h*h + d*d
    
    def diagonal(self):
        return math.sqrt(self.diagonal_sq())

NullRect = Rect3D(0.0,0.0,0.0,0.0,0.0,0.0)
NullRect.swapped_x = False
NullRect.swapped_y = False
NullRect.swapped_z = False

def union_all(kids):
    cur = NullRect
    for k in kids: cur = cur.union(k.rect)
    assert(False ==  cur.swapped_x)
    return cur
