import cv2
from shapely.geometry import LineString, Polygon
import bfs

def draw_obstacles(obstacles, image, obst_size):
    for obst in obstacles:
        cv2.rectangle(image, (obst), (obst[0] + obst_size, obst[1] + obst_size), (0, 0, 0), -1)
    return image

def check_obstacles(obstacles, field, curr_x, curr_y, obstacle_size, point, extr_way=30, stop_dist=30):
    reroute_points = -1
    for obst in obstacles:
        rect_list = [(obst[0], obst[1]), (obst[0], obst[1] + obstacle_size), (obst[0] + obstacle_size, obst[1] + obstacle_size), (obst[0] + obstacle_size, obst[1])]
        #for i in rect_list:
        #    cv2.circle(field, (int(i[0]), int(i[1])), 10, (255, 0, 0), -1)
        line_in_rect = Polygon(rect_list).exterior.intersection(LineString([(curr_x, curr_y), (point[0], point[1])]))
        bnd_points = []

        if line_in_rect:
            bound_points = line_in_rect.bounds
            for shp in line_in_rect:
                x, y = list(shp.coords)[0]
                bnd_points.append((x, y))
                #cv2.circle(field, (int(x), int(y)), 5, (255, 255, 255), -1)


            #Restriction; No support for one point
            #cv2.circle(field, (int(bound_points[0]), int(bound_points[1])), 5, (255, 255, 255), -1)
            #cv2.circle(field, (int(bound_points[2]), int(bound_points[3])), 5, (255, 255, 255), -1)

            # LOCALIZE THE OBSTACLE
            # Get line equation


            line_k = (curr_y - point[1]) / (curr_x - point[0])
            line_b = point[1] - line_k * point[0]

            point_x = bnd_points[0][0] - stop_dist
            point_y = line_k * point_x + line_b
            point_x_1 = bnd_points[1][0] + stop_dist
            point_y_1 = line_k * point_x_1 + line_b
            if curr_x > point[0]: # Left
                point_x, point_x_1 = point_x_1, point_x
                point_y, point_y_1 = point_y_1, point_y
            cv2.circle(field, (int(point_x), int(point_y)), 5, (0, 0, 255), -1)
            cv2.circle(field, (int(point_x_1), int(point_y_1)), 5, (255, 0, 0), -1)




            cv2.line(field, (int(point_x), int(point_y)), (int(point_x), int(point_y - 60)), (0, 0, 255), 2)
            cv2.line(field, (int(point_x_1), int(point_y_1)), (int(point_x_1), int(point_y - 60)), (0, 0, 255), 2)
            cv2.line(field, (int(point_x), int(point_y)), (int(point_x), int(point_y + 60)), (0, 0, 255), 2)
            cv2.line(field, (int(point_x_1), int(point_y_1)), (int(point_x_1), int(point_y + 60)), (0, 0, 255), 2)
            cv2.line(field, (int(point_x), int(point_y - 60)), (int(point_x_1), int(point_y - 60)), (0, 0, 255), 2)
            cv2.line(field, (int(point_x), int(point_y + 60)), (int(point_x_1), int(point_y + 60)), (0, 0, 255), 2)
            maze_size = (int(abs(point_x_1 - point_x)), 120)
            print(f"Generating maze with size {maze_size}")
            if curr_x > point[0]:  # Left direction not finished yet....
                obstacle_x_left = obst[0] - point_x_1 - 10
                obstacle_x_right = obst[0] + obstacle_size - point_x_1 + 10
            else:
                obstacle_x_left = obst[0] - point_x - 10
                obstacle_x_right = obst[0] + obstacle_size - point_x + 10
            print(obstacle_x_left, obstacle_x_right)
            obstacle_y_left = obst[1] - int(point_y - 60) - 10
            obstacle_y_right = obst[1] + obstacle_size - int(point_y - 60) + 10
            print(obstacle_size)

            grid = [[1 if obstacle_x_left <= col <= obstacle_x_right and obstacle_y_left <= row <= obstacle_y_right else 0 for col in range(maze_size[0])] for row in range(maze_size[1])]
            # Dev
            # with open("ways/temp.txt", "w") as file:
            #     file.write(str(grid))
            reroute_points = bfs.main(grid, (0, 60), (maze_size[0], int(point_y_1 - (point_y - 60))), point_x, int(point_y - 60))


            # for pnt in reroute_points:
            #     cv2.circle(field, (int(pnt[0]), int(pnt[1])), 2, (255, 255, 255), -1)

            #no bfs;
            #h = abs(rect_list[0][1] - point_y) + extr_way
            #cv2.line(field, (int(point_x), int(point_y)), (int(point_x), int(point_y - h)), (255, 0, 0), 2)
            #reroute_step_width = 2 * stop_dist + obstacle_size
            #cv2.line(field, (int(point_x), int(point_y - h)), (int(point_x + reroute_step_width), int(point_y - h)), (255, 0, 0), 2)


    return field, reroute_points