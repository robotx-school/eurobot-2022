from ursina import *
from ursina.lights import DirectionalLight, PointLight
from ursina.shaders import lit_with_shadows_shader

TILES = (6, 6)

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
    def __init__(self, map_position=[0, 0], speed=1, movable=False, controls='wasd', **kwargs):
        super().__init__(
            model='assets/robot.obj',
            scale=.5,
            position=coords[map_position[0]][map_position[1]],
            collider='box',
            shader=lit_with_shadows_shader,
            **kwargs
        )
        self.map_position = map_position.copy()
        self.speed = speed
        self.movable = movable
        self.controls = controls
        
        self.speed_sqrt = round(speed / math.sqrt(2), 2)
        
        self.ent = self.Target()
        self.ent.position = coords[self.map_position[0]][self.map_position[1]]
        self.add_script(SmoothFollow(target=self.ent, speed=15))

    def update_position(self):
        for column in range(TILES[0]):
            if abs(coords[column][0][0] - self.ent.position[0]) < coords_cell_distance[0]:
                for row in range(TILES[1]):
                    if abs(coords[0][row][2] - self.ent.position[2]) < coords_cell_distance[1]:
                        self.map_position = (row, column)
                        return

    def update_movement(self):
        direction = [held_keys[self.controls[0]], held_keys[self.controls[1]],
                     held_keys[self.controls[2]], held_keys[self.controls[3]]]

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
                        self.ent.z += self.speed
                if direction[1]:
                    if self.ent.position[0] > coords_limits[0][0]:
                        self.ent.x -= self.speed
                if direction[2]:
                    if self.ent.position[2] > coords_limits[1][1]:
                        self.ent.z -= self.speed
                if direction[3]:
                    if self.ent.position[0] < coords_limits[1][0]:
                        self.ent.x += self.speed
            elif sum(direction) == 2:
                if direction[0]:
                    if self.ent.z < coords_limits[0][1]:
                        self.ent.z += self.speed_sqrt
                if direction[1]:
                    if self.ent.position[0] > coords_limits[0][0]:
                        self.ent.x -= self.speed_sqrt
                if direction[2]:
                    if self.ent.position[2] > coords_limits[1][1]:
                        self.ent.z -= self.speed_sqrt
                if direction[3]:
                    if self.ent.position[0] < coords_limits[1][0]:
                        self.ent.x += self.speed_sqrt

    def update_robot(self):
        self.update_movement()
        self.update_position()

    def move_to(self, x, z):
        self.map_position = [x, z]
        self.ent.position = coords[self.map_position[0]][self.map_position[1]]

    class Target(Entity):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)


def submit():
    global cmd
    cmd = terminal.text
    terminal.text = ''
    terminal.text_field.render()
    terminal.active = False


def input(key):
    if terminal.active:
        if key == 'enter':
            submit()
            
            if cmd == 'unlock':
                camera_free.enabled = True
                camera.enabled = False

            elif cmd == 'lock':
                camera_free.enabled = False
                camera.enabled = True

            elif cmd[:4] == 'move':
                try:
                    robot_1.move_to(*map(int, cmd.split()[1:]))
                except:
                    pass

    else:
        if key == 'enter':
            terminal.active = True


def update():
    distance = [robot_1.x - robot_2.x,
                robot_1.z - robot_2.z]

    if robot_2.intersects().hit:
        if abs(distance[0]) > abs(distance[1]):
            robot_2.ent.position -= (robot_2.speed *
                                     (-1, 1)[distance[0] > 0], 0, 0)
        else:
            robot_2.ent.position -= (0, 0, robot_2.speed *
                                     (-1, 1)[distance[1] > 0])

    robot_1.update_robot()
    robot_2.update_robot()
    
    textbox.text = f'{robot_1.map_position} {robot_2.map_position}'


app = Ursina()
window.title = 'simulator'
window.borderless = False
window.fps_counter.enabled = True
window.exit_button.enabled = False
window.windowed_size = .3
window.update_aspect_ratio()

robot_1 = Robot(color=color.red, map_position=[0, 0], movable=True)
robot_2 = Robot(color=color.green, map_position=[2, 2])
Entity(model='quad', scale=(300, 200),
       rotation_x=90, texture='assets/map.jpg', shader=lit_with_shadows_shader)

camera_free = EditorCamera(
    rotation_smoothing=2, enabled=False, rotation=(30, -30, 0))

camera.position = (300, 300, -300)
camera.rotation_x = 37
camera.rotation_y = -45


DirectionalLight(rotation_x=50, rotation_y=40,
                 shadows=True, color=color.black)

cmd = ''

terminal = InputField(position=(-.39, -.45, 0))
Button('Send', color=color.cyan.tint(-.4),
       position=(-.07, -.45, 0), on_click=submit).fit_to_text()

Text.default_resolution = 1080 * Text.size
textbox = Text(text='', position=(-.63, .48, 0))

app.run()
