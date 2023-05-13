from tk_drawer import TkDrawer
from r2point import R2Point
from convex import Void, Point, Segment, Polygon, setp4

tk = TkDrawer()
f = Void()
tk.clean()

print("Set point for task №4: ")
p4 = R2Point() #заданная точка
setp4(p4)

try:
    while True:
        f = f.add(R2Point())
        tk.clean()
        if isinstance(f, Point):
            tk.draw_point(f.p)
        elif isinstance(f, Segment):
            tk.draw_line(f.p, f.q)
        elif isinstance(f, Polygon):
            for n in range(f.points.size()):
                tk.draw_line(f.points.last(), f.points.first())
                f.points.push_last(f.points.pop_first())
        print(f"S = {f.area()}, P = {f.perimeter()}")
        print(f"Min distance  = {f.min_dist()}")
        print()
except(EOFError, KeyboardInterrupt):
    print("\nStop")
    tk.close()
