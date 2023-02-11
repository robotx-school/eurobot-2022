from robotlib import *

def submit():
    cmd = terminal.text
    terminal.text = ''
    terminal.text_field.render()
    terminal.active = False
    return cmd


def input(key):
    if terminal.active:
        if key == 'enter':
            cmd = submit()

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
    dt = time.dt
    robot_1.update_robot(dt)
    for i in push_bots:
        i.update_robot(dt)


app = Ursina()
application.development_mode = False
window.title = 'simulator'
window.borderless = False
window.fps_counter.enabled = False
window.exit_button.enabled = False
window.update_aspect_ratio()

robot_1 = Robot(color=color.red, map_position=[
                0, 0], mass=5, movable=True, pushable=True)
push_bots = []
for i in range(5):
    push_bots.append(Robot(color=color.white, map_position=[i+1, 5], pushable=True))

eurobot_map = Entity(model='quad', scale=(300, 200),
                     rotation_x=90, texture='assets/map.jpg', shader=lit_with_shadows_shader)

camera_free = EditorCamera(
    rotation_smoothing=2, enabled=False, rotation=(30, -30, 0))

camera.position = (300, 300, -300)
camera.rotation_x = 37
camera.rotation_y = -44


DirectionalLight(rotation_x=50, rotation_y=40,
                 shadows=True, color=color.black)

terminal = InputField(position=(-.39, -.45, 0))
Button('Send', color=color.cyan.tint(-.4),
       position=(-.07, -.45, 0), on_click=submit).fit_to_text()

Text.default_resolution = 1080 * Text.size
textbox = Text(text='', position=(-.63, .48, 0))

app.run()
