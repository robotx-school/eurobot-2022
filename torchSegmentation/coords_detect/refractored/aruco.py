import numpy as np
import cv2
import matplotlib.path as mplPath
import pathlib

final_robots_pixels_coords = []

def find_point(x1_1,y1_1,x1_2,y1_2,x2_1,y2_1,x2_2,y2_2):
    A1 = y1_1 - y1_2
    B1 = x1_2 - x1_1
    C1 = x1_1*y1_2 - x1_2*y1_1
    A2 = y2_1 - y2_2
    B2 = x2_2 - x2_1
    C2 = x2_1*y2_2 - x2_2*y2_1

    if B1*A2 - B2*A1 and A1:
        y = (C2*A1 - C1*A2) / (B1*A2 - B2*A1)
        x = (-C1 - B1*y) / A1
        if min(x1_1, x1_2) <= x <= max(x1_1, x1_2):
            return int(x),int(y)
        else:
            return None
    elif B1*A2 - B2*A1 and A2:
        y = (C2*A1 - C1*A2) / (B1*A2 - B2*A1)
        x = (-C2 - B2*y) / A2
        if min(x1_1, x1_2) <= x <= max(x1_1, x1_2):
            return int(x),int(y)
        else:
            return None
    else:
        return None

def get_coord(image_robots, dictionary, botmarkers, tiles):
    global final_robots_pixels_coords
    bots = [[255, 255], [255, 255], [255, 255], [255, 255]]
    markers = cv2.aruco.detectMarkers(image_robots,dictionary)
    count=0
    for marker in markers[0]:
        x1=int(marker[0][0][0])
        y1=int(marker[0][0][1])
        x2=int(marker[0][1][0])
        y2=int(marker[0][1][1])
        x3=int(marker[0][2][0])
        y3=int(marker[0][2][1])
        x4=int(marker[0][3][0])
        y4=int(marker[0][3][1])
        robot_pos=find_point(x1,y1,x3,y3,x2,y2,x4,y4)
        
        marker_id = markers[1][count][0]
        for i in range(6):
            for j in range(10):
                if tiles[i][j].contains_point(robot_pos):
                    for k in range(len(botmarkers)):
                        if botmarkers[k][0] <= marker_id <= botmarkers[k][-1]:
                            print(k)
                            # our if 0 || 1
                            # enemy if 2 || 3
                            final_robots_pixels_coords.append((robot_pos[0], robot_pos[1], k))
                            if bots[k][0] == 255:
                                bots[k][0] = ((j, i), (j, i-(1, 0)[i == 0]))[k <= 2]
                            else:
                                bots[k][1] = ((j, i), (j, i-(1, 0)[i == 0]))[k <= 2]

        count+=1

    return bots

def find_robots(img):

    botmarkers = [[130, 131, 132, 133], [134, 135, 136, 137], [139, 140, 141, 142], [143, 144, 145, 146]]
    dims = (854, 480)
    dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_250)

    koef_H = [0.11,0.22,0.34,0.5,0.9]
    koef_W = [(0.15,-0.3),(0.23,-0.15),(0.33,0.13),(0.42,0.34),(0.5,0.5),(0.58,0.66),(0.67,0.87),(0.77,1.15),(0.85,1.3)]
    cross_points = []
    tiles=[]
    tiles_coord=[]
    w=dims[0]
    h=dims[1]

    for i in range(-1,len(koef_H)+1):
        row=[]
        if i==-1:
            # x1=0
            # y1=0
            # x2=w
            # y2=0

            x1, y1, x2, y2 = 0, 0, w, 0

        elif i==len(koef_H):
            # x1=0
            # y1=h
            # x2=w
            # y2=h

            x1, y1, x2, y2 = 0, h, w, h

        else:
            # x1=0
            # y1=int(h*koef_H[i])
            # x2=w
            # y2=int(h*koef_H[i])

            x1, y1, x2, y2 = 0, int(h*koef_H[i]), w, int(h*koef_H[i])

        for j in range(-1,len(koef_W)+1):
            if j==-1:
                # x3=0
                # y3=0
                # x4=0
                # y4=h

                x3, y3, x4, y4 = 0, 0, 0, h

            elif j==len(koef_W):
                # x3=w
                # y3=0
                # x4=w
                # y4=h
                
                x3, y3, x4, y4 = w, 0, w, h

            else:
                # x3=int(w*koef_W[j][0])
                # y3=0
                # x4=int(w*koef_W[j][1])
                # y4=h

                x3, y3, x4, y4 = int(w*koef_W[j][0]), 0, int(w*koef_W[j][1]), h

            point=find_point(x1-2000,y1,x2+2000,y2,x3,y3,x4,y4)
            row.append(point)
        cross_points.append(row)
    for i in range(6):
        row=[]
        row_c=[]

        for j in range(10):
            tile_c = ((cross_points[i][j]),
                    (cross_points[i][j+1]),
                    (cross_points[i+1][j+1]),
                    (cross_points[i+1][j]))
            tile = mplPath.Path(np.array([[cross_points[i][j][0], cross_points[i][j][1]],
                                    [cross_points[i][j+1][0], cross_points[i][j+1][1]],
                                    [cross_points[i+1][j+1][0], cross_points[i+1][j+1][1]],
                                    [cross_points[i+1][j][0],cross_points[i+1][j][1]]
                                    ]))
            row.append(tile)
            row_c.append(tile_c)
        tiles.append(row)
        tiles_coord.append(row_c)

    old_data = [[255, 255], [255, 255], [255, 255], [255, 255]]

    
    data = get_coord(img, dictionary, botmarkers, tiles)

    old_c = [item for sublist in old_data for item in sublist].count(255)
    data_c = [item for sublist in data for item in sublist].count(255)

    data = data if data_c <= old_c else old_data

    if old_data != data:
        old_data = data
    return data, final_robots_pixels_coords

if __name__ == "__main__":
    robots_img = cv2.imread("tests/15.jpg")
    print(find_robots(robots_img))
    print(final_robots_pixels_coords)  
    for i in final_robots_pixels_coords:
        cv2.circle(robots_img, (i[0], i[1]), 5, (255, 0, 0), -1)
    cv2.imshow("fff.png", robots_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
