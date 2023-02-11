from ursina import *
from ursina.shaders import lit_with_shadows_shader


#class UI():

class world():
    def __init__(self):
        pass

class Robot():
    def __init__(self, color=color.white, smooth_speed=1 / 100):
        self.model = Entity(model='assets/robot.obj', position=(0, 0, 0), color=color, shader=lit_with_shadows_shader)
        self.coord_changer_coeff = smooth_speed
        self.default_coord_coeff = smooth_speed
    def drive(self, x, y):
        while abs(self.model.x - x) > 0.01 or abs(self.model.z - (-1 * y)) > 0.01:
            if self.model.x != x:
                if self.model.x < x:
                    self.model.x += self.coord_changer_coeff
                else:
                    self.model.x -= self.coord_changer_coeff
            if self.model.z != -1 * y:
                if -1 * y > self.model.z:
                    self.model.z += self.coord_changer_coeff
                else:
                    self.model.z -= self.coord_changer_coeff
        self.model.x = x
        self.model.z = -1 * y
