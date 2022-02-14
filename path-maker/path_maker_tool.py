import threading
import cv2
import numpy as np
from math import degrees, atan2
from termcolor import colored
import json
import obstacles_bypass
from config import *
import collab_system

def recreate_path_side(path):
    # right side converter1
    converted_path = []
    for i in path:
        converted_path.append((903 - i[0], i[1]))
    return converted_path


def rotate_image(image, angle):
    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
    return result


def draw_circle(event, x, y, flags, param):
    global path_curr
    if event == cv2.EVENT_LBUTTONDBLCLK:
        cv2.circle(field, (x, y), 5, (255, 0, 0), -1)
        print("New point:", x, y)
        if AUTO_FIX_POINT: # Not implemented yet
            try:
                if abs(x - path_curr[-1][0]) <= 3:
                    x = path_curr[-1][0]
                elif abs(y - path_curr[-1][1]) <= 3:
                    y = path_curr[-1][1]
            except IndexError:
                pass
        path_curr.append([x, y, 0, 0]) #x, y, action after step, trigger
    if mode == 2:  # for interactive mode No  
        generate_path((x, y))



def interactive_mode_cv(event, x, y, flags, param):
    global robot_1
    if event == cv2.EVENT_LBUTTONDBLCLK:
        cv2.circle(field, (x, y), 5, (255, 0, 0), -1)
        print("New point:", x, y)
        generate_path((x, y))
        Entity(model="cube", scale=(10, 10, 10), position=(x, 1, -1 * y), color=color.red, shader=lit_with_shadows_shader)

        threading.Thread(target=robot_1.drive, args=(x, y)).start()

    elif event == cv2.EVENT_MBUTTONDOWN:
        cv2.rectangle(field, (x, y), (x + obstacle_size, y + obstacle_size), (0, 0, 0), -1)
        obstacles.append((x, y))


def collab_mode_cv(event, x, y, flags, param):
    global sock
    if event == cv2.EVENT_LBUTTONDBLCLK:
        cv2.circle(field, (x, y), 5, (255, 0, 0), -1)
        print("New point:", x, y)
        generate_path((x, y))
        path_curr.append([x, y, 0, 0])
        sock.send(f"{x} {y}".encode("utf-8")) #Send to server

def client_listener(sock):
    global path_curr
    
    while True:
        data = sock.recv(1024).decode("utf-8")
        coords = list(map(int, data.split()))
        print(coords)
        generate_path(coords)
        path_curr.append(coords + [0] * 2)
        print(path_curr)


def convert_to_arduino_string(path):
    
    tmp = str(path).replace("[", "{").replace("]", "}").replace("(", "{").replace(")", "}")
    return f"Dest points[{len(path)}][2] = {tmp}"


def save_path(path, path_name):
    with open(f'{path_name}.json', 'w') as f:
        json.dump(path, f)


def load_path(file_name):
    with open(f'{file_name}.json') as f:
        return json.load(f)


# Vector math
def vect_from_4points(x, y, x1, y1):
    return x1 - x, y1 - y


def angle_between_2vectors(ax, ay, bx, by):
    return degrees(atan2(ax * by - ay * bx, ax * bx + ay * by))


def generate_path(point):
    global curr_x, curr_y, obstacle_name, robot_vect_x, robot_vect_y, points_dest, curr_point_ind, field
    field, reroute = obstacles_bypass.check_obstacles(obstacles, field, curr_x, curr_y, obstacle_size, point)
    if reroute != -1:
        print("Obst reroute", reroute)
        point = [int(reroute[0][0]), int(reroute[0][1])]
        left = points_dest[:curr_point_ind]
        right = points_dest[curr_point_ind + 1:]
        if len(right) == 0:
            right = [points_dest[-1]]
        print(points_dest)
        print(left, right)
        points_dest = left + [point] + reroute + right
        print(points_dest)
    robot_vect, robot_vect_1 = vect_from_4points(curr_x, curr_y, robot_vect_x, robot_vect_y)
    point_vect, point_vect_1 = vect_from_4points(curr_x, curr_y, point[0], point[1])

    angle = angle_between_2vectors(robot_vect, robot_vect_1, point_vect, point_vect_1)
    print(int(((curr_x - point[0]) ** 2 + (curr_y - point[1]) ** 2) ** 0.5))
    dist = one_px * int(((curr_x - point[0]) ** 2 + (curr_y - point[1]) ** 2) ** 0.5)
    route_analytics["dist"] += dist
    if int(angle) != 0:
        route_analytics["rotations"] += 1
    # FEATURE - Debug or LOG to file
    print(colored(f"Angle to rotate: {angle}", "blue"))
    print(colored(f"Distance in millimetrs: {dist}", "yellow"))
    print("---" * 10)
    cv2.arrowedLine(field, (curr_x, curr_y), (point[0], point[1]), (0, 255, 0), 2)

    curr_x, curr_y = point[0], point[1]

    robot_vect_x, robot_vect_y = point[0] + point_vect // 5, point[
        1] + point_vect_1 // 5  # Remake with line equation; Calculate new y using y = kx + b; where x = x + robot_size
    
    cv2.arrowedLine(field, (curr_x, curr_y), (robot_vect_x, robot_vect_y), (255, 0, 0), 5)
    if mode == 1:
        if point[2] != 0:
            cv2.putText(
                field,
                f"Action: {point[2]}", 
                (point[0], point[1]),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 255), 
                2)
        text_coords = point[0], point[1] 
        if point[2] != 0:
            text_coords = point[0], point[1] + 20
        if point[3] != 0:
            cv2.putText(
                field,
                f"Trigger: {point[3]}", 
                (text_coords),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 255), 
                2)
    

def save_path_frontend():
    path_name = input(colored("Name for path file>", "yellow"))
    print(colored(f"Arduino ready array: {convert_to_arduino_string(path_curr)}", "green"))
    try:
        save_path(path_curr, path_name)
        print(colored("Path saved!", "green"))
    except Exception as e:
        print(e)
        print(colored("Error during writing path", "red"))

def live_mode(callback_function=interactive_mode_cv):
    global obstacles, curr_x, curr_y, obstacle_size, obstacle_name, robot_vect_x, robot_vect_y, route_analytics
    path_curr = []
    route_analytics = {"dist": 0, "rotations": 0}
    curr_x, curr_y = 0, 0  # start
    obstacle_size = 50
    robot_vect_x, robot_vect_y = curr_x + robot_size, curr_y

    obstacle_name = 0
    obstacles = []
    cv2.arrowedLine(field, (curr_x, curr_y), (robot_vect_x, robot_vect_y), (0, 0, 255), 5)
    name = 'Interactive mode'
    if callback_function == collab_mode_cv:
        name = "Connected {}:{}".format(*server_address1)
    cv2.namedWindow(name)
    cv2.setMouseCallback(name, callback_function)
    while True:
        cv2.imshow(name, field)
        k = cv2.waitKey(20) & 0xFF
        if k == 27:
            cv2.destroyAllWindows()
            break
        elif k == ord("s"):
            save_path_frontend()



def submit():
    global cmd
    cmd = terminal.text
    terminal.text = ''
    terminal.text_field.render()
    terminal.active = False


if __name__ == "__main__":
    field = cv2.imread(MAP_PATH)
    field = cv2.resize(field, (903, 607))  # consts
    field = rotate_image(field, 180)
    print("Field size: ", field.shape)
    one_px = 2000 / field.shape[0]
    print("Px in mms: ", one_px)
    robot_size = 50  # от этого угол не зависит, но главное, чтобы был > 0
    mode = int(input("Mode (0 - create path; 1 - calculate path; 2 - interactive mode 3 - collab mode )>"))

    if mode == 1:
        name = input(colored("Name for path file>", "yellow"))
        points_dest = load_path(name)
        route_analytics = {"dist": 0, "rotations": 0}
        curr_x, curr_y = START_POINT[0], START_POINT[1]  # start
        obstacle_size = 50
        obstacles = []
        #obstacles = [(375, 225)]
        if SIDE == 1:
            robot_size = -1 * robot_size
            curr_x = 903 - curr_x
            points_dest = recreate_path_side(points_dest)
            print(points_dest)
        robot_vect_x, robot_vect_y = curr_x + robot_size, curr_y

        obstacle_name = 0
        field = obstacles_bypass.draw_obstacles(obstacles, field, obstacle_size)

        cv2.arrowedLine(field, (curr_x, curr_y), (robot_vect_x, robot_vect_y), (0, 0, 255), 5)
        curr_point_ind = 0
        while len(points_dest) > curr_point_ind:
            generate_path(points_dest[curr_point_ind])
            curr_point_ind += 1
        print(colored(
            f"Summary:\nDistance: {route_analytics['dist']}mm\nRotations: {route_analytics['rotations']}\nFinal coordinates: {curr_x, curr_y}",
            "green"))
        print(colored(f"Arduino ready array: {convert_to_arduino_string(points_dest)}", "green"))

        cv2.imshow("Path Gen - Calculated image way", field)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    elif mode == 2:
        threading.Thread(target=live_mode).start()
        from ursina import *
        from ursina.lights import DirectionalLight
        from ursina.shaders import lit_with_shadows_shader
        import visualize_3d

        #Starting 3d
        app = Ursina()
        window.title = 'simulator'
        window.borderless = False
        window.fps_counter.enabled = True
        window.exit_button.enabled = False
        window.windowed_size = .3
        window.update_aspect_ratio()

        robot_1 = visualize_3d.Robot(color=color.green)
        #robot_1.drive(452, 304)

        Entity(model='quad', scale_x = 903, scale_y=607,
            rotation_x=90, rotation_z=180, position=(451, 0, -303), texture='assets/map.jpg', shader=lit_with_shadows_shader)

        camera_free = EditorCamera(
            rotation_smoothing=2, enabled=True, rotation=(30, -30, 0))


        DirectionalLight(rotation_x=50, rotation_y=40,
                        shadows=True, color=color.black)

        
        terminal = InputField(position=(-.39, -.45, 0))
        Button('Send', color=color.cyan.tint(-.4),
            position=(-.07, -.45, 0), on_click=submit).fit_to_text()

        Text.default_resolution = 1080 * Text.size
        textbox = Text(text='', position=(-.63, .48, 0))
        terminal_log = Text(text="", position=window.top_left)

        def input(key):
            if terminal.active:
                if key == 'enter':
                    submit()
                    tmp = cmd.split()
                    if len(tmp) > 1:
                        command, args = tmp[0], ' '.join(tmp[1::])
                    else:
                        command, args = tmp[0], ''
                    if command == 'move':
                        try:
                            threading.Thread(target=robot_1.drive, args=(*map(int, args.split()), )).start()
                        except ValueError:
                            setattr(terminal_log, "text", "Invalid coords: move x y(z in real)")
                            setattr(terminal_log, "color", color.red)
                    elif command == 'locate':
                        setattr(terminal_log, "text", f"X:{robot_1.model.x}\nY:{robot_1.model.y}\nZ:{robot_1.model.z * -1}")
                        setattr(terminal_log, "color", color.white)
            else:
                if key == 'enter':
                    terminal.active = True

        app.run()
    elif mode == 3: #Online collaborative mode
        import socket
        type_of_user = input("Connect to host or start host(c/h)")
        if type_of_user == "h":
            print(f"Starting host on {HOST_LISTEN_FROM}:{HOST_PORT}; Max clients: {HOST_MAX_CLIENTS}")
            
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_address = (HOST_LISTEN_FROM, HOST_PORT)
            sock.bind(server_address)
            sock.listen(HOST_MAX_CLIENTS)
            print("Socket initialized")
            threading.Thread(target=collab_system.host_client_waiter, args=(sock,)).start()
            print("Host waiter thread started\nWaiting clients...")
        else: 
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_address1 = (input("Host IP>"), int(input("Host port>")))
            connected = False
            while not connected:
                try:
                    sock.connect(server_address1)
                    connected = True
                except:
                    print("Retry...")
                    time.sleep(3)
            print('Connected {} port {}'.format(*server_address1))
            path_curr = []
            threading.Thread(target=live_mode, args=(collab_mode_cv, )).start()
            threading.Thread(target=client_listener, args=(sock, )).start()


    elif mode == 0:
        print(
            f"Hotkeys:\nSave path: {colored(chr(HOTKEYS[0]), 'green')}\nConvert to cpp array: {colored(chr(HOTKEYS[1]), 'green')}")
        path_curr = []
        cv2.circle(field, START_POINT, 5, (0, 0, 255), -1)
        cv2.namedWindow('Path creator')
        cv2.setMouseCallback('Path creator', draw_circle)
        cv2.arrowedLine(field, START_POINT, (START_POINT[0] + robot_size, START_POINT[1]), (0, 0, 255), 3)
        while True:
            cv2.imshow('Path creator', field)
            k = cv2.waitKey(20) & 0xFF
            if k == 27:
                exit_confirmation = input(colored("Do you want to save changes?(y/n/c)>", "yellow"))
                if exit_confirmation == "y":
                    save_path_frontend()
                elif exit_confirmation == "c":
                    print("Canceling...")
                else:
                    print("Goodbye")
                    break
            elif k == HOTKEYS[1]:
                print(colored(f"Arduino ready array: {convert_to_arduino_string(path_curr)}", "green"))
            elif k == HOTKEYS[0]:
                save_path_frontend()
            elif k == HOTKEYS[2]:
                cv2.line(field, (START_POINT[0] + robot_size, START_POINT[1]), path_curr[0], (255, 0, 0), 2)
                if len(path_curr) > 2:
                    for pnt in range(len(path_curr) - 1):
                        try:
                            cv2.line(field, path_curr[pnt], path_curr[pnt + 1], (255, 0, 0), 2)
                        finally:
                            pass
            elif k == HOTKEYS[3]:
                #Add action after this step
                print(colored(f"Adding action after step {len(path_curr)}\nStep coords: {path_curr[-1]}", "yellow"))
                action_num = int(input("Action number (1, 2...)"))
                path_curr[-1][2] = action_num
            elif k == HOTKEYS[4]:
                #Add triger to stop
                print(colored(f"Adding trigger to stop while step {len(path_curr)}\nStep coords: {path_curr[-1]}", "yellow"))
                trigger_num = int(input("Trigger number (1, 2...)"))
                path_curr[-1][3] = trigger_num
