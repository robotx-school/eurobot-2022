from ursina import *
from ursina.lights import *
from ursina.shaders import *
from config import *

coords = [[(round(i*(300-24)/TILES[0] + 12 - 150, 1), 0, round(100 - (j*(200-24)/TILES[1] + 12), 2))
           for j in range(TILES[1] + 1)] for i in range(TILES[0] + 1)]

coords_cell_distance = (
    abs(coords[0][0][0] - coords[1][0][0]), abs(coords[0][0][2] - coords[0][1][2]))

coords_limits = ((coords[0][0][0], coords[0][0][2]),
                 (coords[TILES[0]][TILES[1]][0], coords[TILES[0]][TILES[1]][2]))


def mm_to_units(x, y, z):
    return ((x/10-150, -150)[x == 0], (y/10, 0)[y == 0], (-z/10+100, 100)[z == 0])


def units_to_mm(x, y, z):
    return (round((x+150)*10), round(y/10), round((-z+100)*10))


class Robot(Entity):
    def __init__(self, map_position=[0, 0], mass=1, speed=.5, movable=False, controls='wasd', pushable=False, **kwargs):
        super().__init__(
            model='assets/robot.obj',
            scale=.5,
            position=coords[map_position[0]][map_position[1]],
            collider='box',
            shader=lit_with_shadows_shader,
            **kwargs
        )
        self.map_position = map_position.copy()
        self.mass = 2 / mass
        self.speed = speed
        self.movable = movable
        self.controls = controls
        self.pushable = pushable

        self.speed_sqrt = round(speed / math.sqrt(2), 2)

        self.ent = self.Target()
        self.ent.position = coords[self.map_position[0]][self.map_position[1]]
        self.add_script(SmoothFollow(target=self.ent, speed=SMOOTH_SPEED))

    def update_position(self):
        for column in range(TILES[0]):
            if abs(coords[column][0][0] - self.ent.position[0]) < coords_cell_distance[0] + self.speed * 2:
                for row in range(TILES[1]):
                    if abs(coords[0][row][2] - self.ent.position[2]) < coords_cell_distance[1] + self.speed * 2:
                        self.map_position = (row, column)
                        return

    def update_movement(self, dt):
        direction = [held_keys[self.controls[0]], held_keys[self.controls[1]],
                     held_keys[self.controls[2]], held_keys[self.controls[3]]]
        dt *= 100

        if self.ent.z > coords_limits[0][1]:
            self.ent.z = coords_limits[0][1]
        if self.ent.position[0] < coords_limits[0][0]:
            self.ent.x = coords_limits[0][0]
        if self.ent.position[2] < coords_limits[1][1]:
            self.ent.z = coords_limits[1][1]
        if self.ent.position[0] > coords_limits[1][0]:
            self.ent.x = coords_limits[1][0]

        if self.movable:
            if sum(direction) == 1:
                if direction[0]:
                    if self.ent.z < coords_limits[0][1]:
                        self.ent.z += self.speed * dt
                if direction[1]:
                    if self.ent.position[0] > coords_limits[0][0]:
                        self.ent.x -= self.speed * dt
                if direction[2]:
                    if self.ent.position[2] > coords_limits[1][1]:
                        self.ent.z -= self.speed * dt
                if direction[3]:
                    if self.ent.position[0] < coords_limits[1][0]:
                        self.ent.x += self.speed * dt
            elif sum(direction) == 2:
                if direction[0]:
                    if self.ent.z < coords_limits[0][1]:
                        self.ent.z += self.speed_sqrt * dt
                if direction[1]:
                    if self.ent.position[0] > coords_limits[0][0]:
                        self.ent.x -= self.speed_sqrt * dt
                if direction[2]:
                    if self.ent.position[2] > coords_limits[1][1]:
                        self.ent.z -= self.speed_sqrt * dt
                if direction[3]:
                    if self.ent.position[0] < coords_limits[1][0]:
                        self.ent.x += self.speed_sqrt * dt

        if self.pushable:
            if self.intersects().hit:
                distance = [self.intersects().entity.position[0] - self.x,
                            self.intersects().entity.position[2] - self.z]
                if abs(distance[0]) > abs(distance[1]):
                    self.ent.position -= (dt * self.mass *
                                          (-1, 1)[distance[0] > 0], 0, 0)
                else:
                    self.ent.position -= (0, 0, dt * self.mass *
                                          (-1, 1)[distance[1] > 0])

    def update_robot(self, dt):
        self.update_movement(dt)
        self.update_position()

    def move_to(self, x, z):
        self.map_position = [x, z]
        self.ent.position = coords[self.map_position[0]][self.map_position[1]]

    class Target(Entity):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
