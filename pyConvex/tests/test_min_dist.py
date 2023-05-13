from pytest import approx
from math import sqrt
from r2point import R2Point
from convex import Figure, Void, Point, Segment, Polygon

		
# MIN DIST TESTS

#point

def test_min_dist1():
	f = Void()
	p4 = R2Point(0.0, 0.0)
	f = f.add(R2Point(0.0, 0.0))
	assert f.min_dist() == 0.0

def test_min_dist2():
	p4 = R2Point(0.0, 0.0)
	f = Void()
	f = f.add(R2Point(4.0, 3.0))
	assert f.min_dist() == 5.0

# segment
def test_min_dist3():
	p4 = R2Point(0.0, 0.0)
	f = Void()
	f = f.add(R2Point(4.0, 3.0))
	f = f.add(R2Point(8.0, 6.0))
	assert f.min_dist() == 5.0

def test_min_dist4():
	p4 = R2Point(0.0, 0.0)
	f = Void()
	f = f.add(R2Point(6.0, 8.0))
	f = f.add(R2Point(3.0, 4.0))
	assert f.min_dist() == 5.0

# polygon
def test_min_dist5():
	p4 = R2Point(0.0, 0.0)
	f = Void()
	f = f.add(R2Point(1.0, 3.0))
	f = f.add(R2Point(1.0, 0.0))
	f = f.add(R2Point(6.0, 8.0))
	assert f.min_dist() == 1.0

def test_min_dist6():
	p4 = R2Point(0.0, 0.0)
	f = Point(R2Point(1.0, 3.0))
	f = f.add(R2Point(1.0, 0.0))
	f = f.add(R2Point(3.0, 4.0))
	f = f.add(R2Point(6.0, 8.0))
	assert f.min_dist() == 1.0

def test_min_dist6():
	p4 = R2Point(0.0, 0.0)
	f = Void()
	f = f.add(R2Point(1.0, 3.0))
	f = f.add(R2Point(1.0, 0.0))
	f = f.add(R2Point(3.0, 4.0))
	f = f.add(R2Point(6.0, 8.0))
	f = f.add(R2Point(2.0, 2.0))
	assert f.min_dist() == 1.0

