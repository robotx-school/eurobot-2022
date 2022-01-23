import cv2
import numpy as np
from math import degrees, atan2, fabs, pow
from termcolor import colored
from shapely.geometry import LineString, Polygon
import json
import bfs_back

def rotate_image(image, angle):
    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
    return result

def draw_circle(event,x,y,flags,param):
    global path_curr
    if event == cv2.EVENT_LBUTTONDBLCLK:
        cv2.circle(field,(x,y),5,(255,0,0),-1)
        print("New point:", x,y)
        path_curr.append((x, y))

#Vecor math
def vect_from_4points(x, y, x1, y1):
    return x1 - x, y1 - y
def angle_between_2vectors(ax, ay, bx, by):
    return degrees(atan2( ax*by - ay*bx, ax*bx + ay*by))

#Other functions
def getDis(pointX, pointY, lineX1, lineY1, lineX2, lineY2):
    a = lineY2 - lineY1
    b = lineX1 - lineX2
    c = lineX2 * lineY1 - lineX1 * lineY2
    dis = (fabs(a * pointX + b * pointY + c)) / (pow(a * a + b * b, 0.5))
    return dis
def generate_path(point):
    global curr_x, curr_y, obstacle_name, robot_vect_x, robot_vect_y
    line_list = [(curr_x, curr_y), (point[0], point[1])] 
    intersection = (0, 255, 0)
    
    for obst in obstacles:
        rect_list = [(obst[0], obst[1]), (obst[0], obst[1] + obstacle_size), (obst[0] + obstacle_size, obst[1] + obstacle_size), (obst[0] + obstacle_size, obst[1])]
        
        line_in_rect = Polygon(rect_list).intersection(LineString(line_list))
        
        if line_in_rect:
            bound_points = line_in_rect.bounds
            print(colored(f"Obstacle on way, length through it: {bound_points}", "red"))
            #Restriction; No support for one point
            cv2.circle(field, (int(bound_points[0]), int(bound_points[1])), 5, (255, 255, 255), -1)
            cv2.circle(field, (int(bound_points[2]), int(bound_points[3])), 5, (255, 255, 255), -1)
            maze_size = (abs(point[0] - curr_x), abs(point[1] - curr_y))
            
            # Get line equation
            line_k = (curr_y - point[1]) / (curr_x - point[0])
            line_b = point[1] - line_k * point[0]
            
            #NO BFS IMPELEMENTATION
            box_left_x = int(bound_points[0]) - 30
            box_left_y = int((bound_points[0] - 30) * line_k + line_b - obstacle_size)
            box_bottom_x = int(bound_points[2]) + 30
            box_bottom_y = int((bound_points[2] + 30) * line_k + line_b)
            #cv2.circle(field, (box_left_x, box_left_y), 5, (0, 0, 255), -1)
            #cv2.circle(field, (box_bottom_x, box_bottom_y), 5, (0, 0, 255), -1)
            #Recreate new way
            point = (box_left_x, box_left_y + obstacle_size)
            cv2.arrowedLine(field, (box_left_x, box_left_y + obstacle_size), (box_left_x, box_left_y), (0, 0, 0), 3)
            cv2.arrowedLine(field, (box_left_x, box_left_y), (box_bottom_x, box_left_y), (0, 0, 0), 3)
            cv2.arrowedLine(field, (box_bottom_x, box_left_y), (box_bottom_x, box_bottom_y), (0, 0, 0), 3)
            
            #Localize it to use in maze
            cv2.circle(field, (obst[0], obst[1]), 5, (255, 0, 0), -1) #Top left corner
            cv2.circle(field, (obst[0] + obstacle_size, obst[1] + obstacle_size), 5, (255, 0, 0), -1) #Bottom right corner
            obstacle_x_left = obst[0] - curr_x
            obstacle_x_right = obst[0] - curr_x + obstacle_size
            obstacle_y_left = obst[1] - curr_y
            obstacle_y_right = obst[1] - curr_y + obstacle_size
            
            grid = [[1 if obstacle_x_left <= col <= obstacle_x_right and obstacle_y_left <= row <= obstacle_y_right else 0 for col in range(maze_size[0])] for row in range(maze_size[1])]
            #for y in range(len(grid)):
            #    for x in range(len(grid[y])):
            #        pass
            print(colored(f"Generating maze for bfs: {maze_size}\nData file: {obstacle_name}", "cyan"))
            
            with open(f'grid_data_{obstacle_name}.txt', 'w') as fw:
                json.dump(grid, fw)
            obstacle_name += 1
            
            '''
            Legacy; static way recreation
            detour_point = int(bound_points[0]), int(bound_points[1]) - 50
            detour_point_1 = int(bound_points[0]) + 80, int(bound_points[1]) - 50
            cv2.circle(field, (int(bound_points[0]), int(bound_points[1])), 5, (255, 255, 255), -1)
            cv2.arrowedLine(field, (int(bound_points[0]), int(bound_points[1])), detour_point, (255, 255, 255), 2)
            cv2.arrowedLine(field, detour_point, detour_point_1, (255, 255, 255), 2)
            dist_to_way = int(getDis(detour_point_1[0], detour_point_1[1], curr_x, curr_y, point[0], point[1]))
            print(dist_to_way)
            cv2.arrowedLine(field, detour_point_1, (detour_point_1[0], detour_point_1[1] + dist_to_way), (255, 255, 255), 2)
            cv2.circle(field, (int(bound_points[2]), int(bound_points[3])), 5, (255, 255, 255), -1)
            '''
            intersection = (0, 0, 255)

    robot_vect, robot_vect_1 = vect_from_4points(curr_x, curr_y, robot_vect_x, robot_vect_y)
    point_vect, point_vect_1 = vect_from_4points(curr_x, curr_y, point[0], point[1])
    
    angle = angle_between_2vectors(robot_vect, robot_vect_1, point_vect, point_vect_1)
    dist = one_px * int(((curr_x - point[0]) ** 2 + (curr_y - point[1]) ** 2) ** 0.5)
    route_analytics["dist"] += dist
    if int(angle) != 0:
        route_analytics["rotations"] += 1
    #FEATURE - Debug or LOG to file
    print(colored(f"Angle to rotate: {angle}", "blue"))
    print(colored(f"Distance in millimetrs: {dist}", "yellow"))
    print("---" * 10)
    cv2.arrowedLine(field, (curr_x, curr_y), (point[0], point[1]), intersection, 2)
    try: #One time 
        k = (curr_y - point[1]) / (point[0] - curr_x)
        b = point[1] - k * point[0]
        curr_x, curr_y = point[0], point[1]
        
        robot_vect_x, robot_vect_y = point[0] + point_vect // 5, point[1] + point_vect_1 // 5 #Remake with line equation; Caluclate new y using y = kx + b; where x = x + robot_size

        cv2.arrowedLine(field, (curr_x, curr_y), (robot_vect_x, robot_vect_y), (255, 0, 0), 5)
    except:
        pass

field = cv2.imread("map.jpg")
field = cv2.resize(field, (903, 607))
field = rotate_image(field, 180)
print("Field size: ", field.shape)
one_px = field.shape[0] / 2000
print("Px in mms: ", one_px)
robot_size = 50 #от этого угол не зависит, но главное, чтобы был > 0
mode = int(input("Mode (0 - create path; 1 - calculate path)>"))
if mode:
    route_analytics = {"dist": 0, "rotations": 0}
    curr_x, curr_y = 28, 412 #start
    obstacle_size = 50

    
    robot_vect_x, robot_vect_y = curr_x + robot_size, curr_y
    try: #Remake with json
        import path
        points_dest = path.dst
    except:
        print(colored("Default", "red")) 
        points_dest = [(100, 100),
                    (230, 400), 
                    (400, 400),
                    (400, 300),
                    (495, 204),
                    (608, 345)]
    obstacles = [(349, 166), (302, 525), (267, 336), (534, 347)]
    obstacle_name = 0
    for obst in obstacles:
        cv2.rectangle(field, (obst[0], obst[1]), (obst[0] + obstacle_size, obst[1] + obstacle_size), (0, 0, 0), -1)
    cv2.arrowedLine(field, (curr_x, curr_y), (robot_vect_x, robot_vect_y), (0, 0, 255), 5)
    curr_point_ind = 0
    while len(points_dest) > curr_point_ind:
        generate_path(points_dest[curr_point_ind])
        curr_point_ind += 1
    print(colored(f"Summary:\nDistance: {route_analytics['dist']}mm\nRotations: {route_analytics['rotations']}", "green"))  

    cv2.imshow("Path Gen - Calculated image way", field)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    path_curr = []
    cv2.namedWindow('Path creator')
    cv2.setMouseCallback('Path creator', draw_circle)
    while(1):
        cv2.imshow('Path creator', field)
        k = cv2.waitKey(20) & 0xFF
        if k == 27:
            break
        elif k == ord("s"):
            print("Saving path to 'path.py (MODULE)'")
            with open("path.py", "w") as path_writer:
                path_writer.write(f"dst = {str(path_curr)}")

