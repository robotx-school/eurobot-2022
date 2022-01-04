
import socket
import cv2
import pickle
import struct
from net import Net
import numpy as np

print("Loading model...")
net = Net("model.t")
print("Model loaded")

#TCP
sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address1 = ('192.168.0.188', 10006)
connected = False
while not connected:
    try:
        sock1.connect(server_address1)
        connected = True
    except:
        print("Retry...")
        time.sleep(3)

print('Подключено к {} порт {}'.format(*server_address1))
data = b''
payload_size = struct.calcsize("I")
while True:
    while len(data) < payload_size:
        data += sock1.recv(4096)
    packed_msg_size = data[:payload_size]
 
    data = data[payload_size:]
    msg_size = struct.unpack("I", packed_msg_size)[0]
    
    while len(data) < msg_size:
        data += sock1.recv(4096)
    frame_data = data[:msg_size]
    data = data[msg_size:]
 
    frame = pickle.loads(frame_data)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    cv2.imwrite('aa.png', frame)
    img, mask = net.get_colored_img(frame)
    '''
    Coord recognition
    cv2.imwrite('cam.png', img)

    img = cv2.resize(img, (256, 256))

    mask = np.where(mask[0, :, :] == 1, 255, 0)
    cv2.imwrite("mask.png", mask)
    m = cv2.imread("mask.png")
    m = cv2.cvtColor(m, cv2.COLOR_RGB2GRAY)
    cv2.line(m, (0, 10), (1024, 10), (0, 255, 0))

    contours, hierarchy = cv2.findContours(m,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_TC89_L1)
    mm = cv2.moments
    mm = list(map(cv2.moments, contours))
    moments = [i["m00"] for i in map(cv2.moments, contours)]
    contours = list(contours)
    c = 0
    final = []
    robots_coords = []
    for i in map(cv2.moments, contours):
        if i["m00"] >= 2500:
            final.append(contours[c])
            cx = int(i['m10']/i['m00'])
            cy = int(i['m01']/i['m00'])
            
            
            new_coords = (cx, cy)
            cv2.putText(m, f"{new_coords[0]}; {new_coords[1]}", (cx - 20, cy - 15),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
            print(f"x: {new_coords[0]} y: {new_coords[1]}")
            robots_coords.append(new_coords)
            
        else:
            cv2.drawContours(m, (contours[c]), -1, (0, 0, 0), 3, cv2.FILLED)
            cv2.fillPoly(m, pts =[contours[c]], color=(0,0,0))

        c += 1
    print("Coords: ", robots_coords)
    
    m = cv2.cvtColor(m, cv2.COLOR_GRAY2RGB)
    cv2.drawContours(m, final, -1, (0, 255,0), 3, cv2.FILLED)
    cv2.fillPoly(m, final, color=(0,255,0))

    cv2.imwrite("resulted_mask.png", m)
    ''' 
    sock1.send(b"100 100") # fake coords

