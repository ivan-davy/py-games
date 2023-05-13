from r2point import R2Point
from convex import Void, setp4

f = Void()

print(f"Set point for task №4: ")
p4 = R2Point() # заданная точка
setp4(p4)
print()

try:
    while True:
        print(f"Convex point: ")
        f = f.add(R2Point())
        print(f"S = {f.area()}, P = {f.perimeter()}")
        print(f"Min distance  = {f.min_dist()}")
        print()

except(EOFError, KeyboardInterrupt):
    print("\nStop")
