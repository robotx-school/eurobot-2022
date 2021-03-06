import numpy as np
import cv2
import matplotlib.path as mplPath
import struct
import serial
from datetime import datetime
import pathlib

# logging_dir = '/home/pi/net/aruco/logs/'
# pathlib.Path(logging_dir).mkdir(parents=True, exist_ok=True)

# filename = logging_dir + str(datetime.now().strftime("%Y-%m-%d-%H-%M-%S")) + '.log'
# open(filename, 'w').close()

field = cv2.imread("field.png")
field = cv2.cvtColor(field,cv2.COLOR_BGR2GRAY)
field = cv2.cvtColor(field,cv2.COLOR_GRAY2BGR)
field = cv2.resize(field, (1920,1080), interpolation = cv2.INTER_AREA)
marked_field = field.copy()

botmarkers = [[130, 131, 132, 133], [134, 135, 136, 137], [139, 140, 141, 142], [143, 144, 145, 146]]

# port = serial.Serial('COM5', 115200, timeout=1)
port = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
port.flush()

# dims = (854, 480)
dims = (1280, 720)

h, w = dims

cap = cv2.VideoCapture(0)
cap.set(3, dims[0])
cap.set(4, dims[1])

dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_250)

def findX(xshift, lean, yshift, y):
    x = (y - yshift) / lean - xshift
    return int(x)

def findY(xshift, lean, yshift, x):
    y = (x + xshift) * lean + yshift
    return int(y)

def locateinSquares(Rx,Ry):
    global hlines,vlines

    for i in range(9):
        if findX(vlines[i][0], vlines[i][1], vlines[i][2], Ry) < Rx:
            xKvadrat = i + 1

    for i in range(5):
        if findY(hlines[i][0], hlines[i][1], hlines[i][2], Rx) < Ry:
            yKvadrat = i + 1

    # print(xKvadrat,yKvadrat)

def drawLines(xshift, lean, yshift):
    for x in range (w):
        y = (x + xshift) * lean + yshift
        y = int(y)
        cv2.line(img, (x, y), (x + 1, int((1 + x + xshift) * lean + yshift)), (255, 255, 0), 7)
        # cv2.circle(img,(x,y),7,(255,255,0),-1)

def findAruco(img):
    global centers
    markers = cv2.aruco.detectMarkers(img, dictionary)

    for i in range(len(markers[0])):
        x1 = int(markers[0][i][0][0][0])
        y1 = int(markers[0][i][0][0][1])
        
        x2 = int(markers[0][i][0][1][0])
        y2 = int(markers[0][i][0][1][1])
        
        x3 = int(markers[0][i][0][2][0])
        y3 = int(markers[0][i][0][2][1])
        
        x4 = int(markers[0][i][0][3][0])
        y4 = int(markers[0][i][0][3][1])

        center = fp(x1, y1, x3, y3, x2, y2, x4, y4)
        centers.append(center)

def grid(img):
    for i in range(10):
        cv2.line(img, (img.shape[1] // 10 * (i + 1), 0),(img.shape[1] // 10 * (i + 1), img.shape[0]),((151), (151), (55)), 5)
    
    for i in range(7):
        cv2.line(img, (0, (img.shape[0] // 7) * (i + 1)),(img.shape[1], (img.shape[0] // 7) * (i + 1)),((151), (151), (55)), 5)
    
    return img

def log_coord(coord, filename):
    with open(filename, 'a') as file:
        file.write(format(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' -- ' + str(coord) + '\n'))

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

def get_coord_img(image_robots, image_field):
    koef_H=[0.11,0.22,0.34,0.5,0.9]
    koef_W=[(0.15,-0.3),(0.23,-0.15),(0.33,0.13),(0.42,0.34),(0.5,0.5),(0.58,0.66),(0.67,0.87),(0.77,1.15),(0.85,1.3)]
    gray = cv2.cvtColor(image_robots,cv2.COLOR_BGR2GRAY)
    image_robots = cv2.cvtColor(gray,cv2.COLOR_GRAY2RGB)
    h=image_robots.shape[0]
    w=image_robots.shape[1]
    cross_points=[]
    tiles=[]
    tiles_coord=[]
    for i in range(-1,len(koef_H)+1):
        row=[]
        if i==-1:
            x1=0
            y1=0
            x2=w
            y2=0
        elif i==len(koef_H):
            x1=0
            y1=h
            x2=w
            y2=h
        else:
            x1=0
            y1=int(h*koef_H[i])
            x2=w
            y2=int(h*koef_H[i])
        cv2.line(image_robots,(x1,y1),(x2,y2),(128,128,0),5)
        for j in range(-1,len(koef_W)+1):
            if j==-1:
                x3=0
                y3=0
                x4=0
                y4=h
            elif j==len(koef_W):
                x3=w
                y3=0
                x4=w
                y4=h
            else:
                x3=int(w*koef_W[j][0])
                y3=0
                x4=int(w*koef_W[j][1])
                y4=h
            cv2.line(image_robots,(x3,y3),(x4,y4),(128,0,128),5)
            point=find_point(x1-2000,y1,x2+2000,y2,x3,y3,x4,y4)
            row.append(point)
            #print(i,j,point,x1,y1,x2,y2,x3,y3,x4,y4)
        #print()
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

    markers = cv2.aruco.detectMarkers(img,dictionary)
    count=0
    for i in range(0,w,w//10):
        for j in range(0,h,h//7):
            t=3
            c=(255,128,0)
            c1=(i,j)
            c2=(i+w//10,j+h//7)
            cv2.rectangle(image_field, c1, c2, c, t)
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
        cv2.circle(image_robots,robot_pos,15,(0,0,120),-1)
        for i in range(6):
            for j in range(10):
                if tiles[i][j].contains_point(robot_pos):
                    # print(i,j)
                    pos=(j,i)
                    cv2.line(image_robots,tiles_coord[i][j][-1],tiles_coord[i][j][0],(128,0,0),8)
                    cv2.line(image_robots,tiles_coord[i][j][0],tiles_coord[i][j][1],(128,0,0),8)
                    cv2.line(image_robots,tiles_coord[i][j][1],tiles_coord[i][j][2],(128,0,0),8)
                    cv2.line(image_robots,tiles_coord[i][j][2],tiles_coord[i][j][3],(128,0,0),8)
                    cv2.rectangle(image_field, ((j*w//10),(i*h//7)), ((j*w//10)+w//10,(i*h//7)+h//7), (255,0,255), 5)
        count+=1
    scale= 30
    width = int(image_robots.shape[1] * scale / 100)
    height = int(image_robots.shape[0] * scale / 100)
    dim = (width, height)
    image_robots = cv2.resize(image_robots, dim, interpolation = cv2.INTER_AREA)
    image_field = cv2.resize(image_field, dim, interpolation = cv2.INTER_AREA)
    image_res = np.vstack([image_robots,image_field])
    return image_res

def get_coord(image_robots, dictionary, botmarkers):
    positions={}
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
                    if marker_id in botmarkers[2] or marker_id in botmarkers[3]:
                        positions[marker_id] = (j,i+1)
                    else:
                        positions[marker_id] = (j,i)
        count+=1
    for i in range(len(botmarkers)):
        for j in range(len(botmarkers[i])):
            if botmarkers[i][j] in positions.keys():
                bots[i][j-2 if j>=2 else j] = (positions[botmarkers[i][j]])

    return bots

koef_H=[0.11,0.22,0.34,0.5,0.9]
koef_W=[(0.15,-0.3),(0.23,-0.15),(0.33,0.13),(0.42,0.34),(0.5,0.5),(0.58,0.66),(0.67,0.87),(0.77,1.15),(0.85,1.3)]
cross_points=[]
tiles=[]
tiles_coord=[]
w=dims[0]
h=dims[1]

for i in range(-1,len(koef_H)+1):
    row=[]
    if i==-1:
        x1=0
        y1=0
        x2=w
        y2=0
    elif i==len(koef_H):
        x1=0
        y1=h
        x2=w
        y2=h
    else:
        x1=0
        y1=int(h*koef_H[i])
        x2=w
        y2=int(h*koef_H[i])
    for j in range(-1,len(koef_W)+1):
        if j==-1:
            x3=0
            y3=0
            x4=0
            y4=h
        elif j==len(koef_W):
            x3=w
            y3=0
            x4=w
            y4=h
        else:
            x3=int(w*koef_W[j][0])
            y3=0
            x4=int(w*koef_W[j][1])
            y4=h
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

while True:
    # img = cv2.imread('test.jpg')
    _, img = cap.read()

    data = get_coord(img, dictionary, botmarkers)
    img_robot = get_coord_img(img, marked_field)

##    if old_data != data:
##        if not pathlib.Path(filename).is_file():
##            open(filename, 'w').close()
##
##        log_coord(data, filename)
##        old_data = data

    raw_data = sum(data, [])

    for i in range(len(raw_data)):
        if isinstance(raw_data[i], tuple):
            raw_data[i] = raw_data[i][0]<<4 | raw_data[i][1]

    byte_data = struct.pack('cccccccc',
                raw_data[0].to_bytes(1, "big"),
                raw_data[1].to_bytes(1, "big"),
                raw_data[2].to_bytes(1, "big"),
                raw_data[3].to_bytes(1, "big"),
                raw_data[4].to_bytes(1, "big"),
                raw_data[5].to_bytes(1, "big"),
                raw_data[6].to_bytes(1, "big"),
                raw_data[7].to_bytes(1, "big"),)

    port.write(byte_data)

    print(data)

    cv2.imshow("camera",img_robot)

    if cv2.waitKey(1) & 0xFF == ord('q'):
            break
cap.release()
cv2.destroyAllWindows()
