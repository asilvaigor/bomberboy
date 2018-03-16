from source.core.map.Grid import *
import random
import time

Matrix = Grid()

print(Matrix.__getattr__(position=(2, 3)))

dimension = Matrix.get_dimension()

while True:
    position = (random.randint(1, dimension[0]-2), random.randint(1, dimension[1] - 2))
    event = random.randint(3, 8)
    print(position, event)
    Matrix.update(position, event)
    print(Matrix.get_tilemap())
    time.sleep(2)