import torch
from torchvision import transforms
import cv2
import numpy as np
import aruco
from colorama import init, Fore
import time, traceback
import itertools


#Global CONF
FAKE_ARUCO_COUNT = 3 # -1 to disable fake count
DEBUG_MODE = 1 #DEBUG - 1; PRODUCTION - 0 #PRODUCTION only errors writing in log file
PROFILER = 0 #1 - enable time measuring for key features
DRAW_VISUAL_ITEMS = 1 #draw lines circle to see opencv and net results on image


class Net:
    def __init__(self, model_path):
        self.DEVICE = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
        self.net = torch.load(model_path, map_location=self.DEVICE)
    def get_segment_labels(self, image, model):
        image = image.to(self.DEVICE)
        model.eval()
        outputs = model(image)
        return outputs['out'][0]

    def get_colored_img(self, _image_, size=(512, 512)):
        img = cv2.cvtColor(_image_, cv2.COLOR_BGR2RGB)
        #img = cv2.resize(img, size)
        preprocess = transforms.Compose([
            transforms.ToTensor(),
        ])

        norm_img = preprocess(img / 255)
        input_tensor = norm_img.to(torch.float)
        input_batch = input_tensor.unsqueeze(0)
        pred = self.get_segment_labels(input_batch, self.net)
        labels = pred.detach().cpu().numpy()
        labels = np.where(labels > 0.5, 1, 0)
        img[:, :, 1] = np.where(labels[0, :, :] == 1, 0, img[:, :, 1])
        img[:, :, 2] = np.where(labels[0, :, :] == 1, 0, img[:, :, 2])
        return img, labels

class Image:
    def __init__(self):
        self.img1 = np.zeros((1024, 1024, 3), np.uint8) #black image 1024 x 1024 
        self.points = np.float32([[254, 656], [766, 655], [266, 438], [712, 440]])
    def concatinate_images(self, img1, img2):
        brows, bcols = img1.shape[:2]
        rows, cols, _ = img2.shape
        roi = img1[int(brows / 2) - int(rows / 2) : int(brows / 2) + int(rows / 2), int(bcols / 2)- 
        int(cols / 2) : int(bcols / 2) + int(cols / 2)]

        img2gray = cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)
        ret, mask = cv2.threshold(img2gray, 10, 255, cv2.THRESH_BINARY)
        mask_inv = cv2.bitwise_not(mask)

        img1_bg = cv2.bitwise_and(roi, roi, mask = mask_inv)

        img2_fg = cv2.bitwise_and(img2, img2, mask = mask)

        dst = cv2.add(img1_bg,img2_fg)
        img1[int(brows / 2) - int(rows / 2) : int(brows / 2) + int(rows / 2), int(bcols / 2)- 
        int(cols / 2) : int(bcols / 2) + int(cols / 2) ] = dst
        return img1
    def corerct_perspective(self, image):
        ''' Point Top Left -> (0; 0)
            Point Bottom Left((0; 0)) -> остаётся на месте
            Point Top Right -> (1024; 0); 1024 - image width
            Point Bottom Right((1024; 1024)) -> остаётся на месте
        '''
        old_width = image.shape[0]
        old_height = image.shape[1]
        img2 = cv2.resize(image, (512, 288))
        img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
        res = self.concatinate_images(self.img1, img2)
        output_pts = np.float32([[254, 656], [766, 655], [0, 0], [res.shape[1], 0]])
        M = cv2.getPerspectiveTransform(self.points, output_pts)
        out = cv2.warpPerspective(res, M, (res.shape[1], res.shape[0]), flags=cv2.INTER_LINEAR)
        return out, (old_width, old_height)

class Robots:
    def __init__(self, img):
        self.aruco_data, self.robots_pixels = aruco.find_robots(img)
        self.img = img
    def recheck_aruco(self, img):
        self.aruco_data, self.robots_pixels = aruco.find_robots(img)
        self.img = img
    def robots_count_aruco(self):
        robots_count = 0
        for i in self.aruco_data:
            if i[0] != 255 or i[1] != 255:
                robots_count += 1
        if FAKE_ARUCO_COUNT != -1:
            robots_count = FAKE_ARUCO_COUNT #на имеющихся тестовых данных на некоторых роботах нет маркера (16.jpg)
        return robots_count, self.robots_pixels
    def get_cell_by_px(self, pxs):        
        bottom_x, bottom_y = pxs[0], pxs[1]
        new_coords = [bottom_x, bottom_y]

        width_px = (512 - 37) // 10 #horizontal width of cell; 37 left border distance
        height_px = 32#vertical height of cell
        robot_x, robot_y = bottom_x, bottom_y - 15 #15 - height less

        new_coords[0] = 10 - (robot_x // width_px) - 1 
        new_coords[1] = 10 - (robot_y // height_px) - 1
        return new_coords
    

class Logger:
    def __init__(self, log_path):
        self.log_path = log_path
        with open(log_path, "w") as file:
            file.write("[INFO] Program started")
    def write_log(self, message):
        with open(self.log_path, "a") as file:
            file.write(f"[ERROR][{str(time.ctime())}] {message} \n")

def rotate_image(image, angle):
    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
    return result



#initing logger first
letters_for_robots = ["A", "B", "C", "D"] #Legacy but useful
if DEBUG_MODE == 0:
    start_time = time.ctime()
    start_time = str(start_time).replace(":", "-")
    log = Logger(f"logs/{start_time}.txt")
if DEBUG_MODE:
    print(Fore.YELLOW + f"[INFO] Loading model...")
try:
    net = Net("model.t")
    print(Fore.YELLOW + f"[INFO] Torch running on {net.DEVICE}")
except: 
    if not DEBUG_MODE: #log
        log.write_log(str(traceback.format_exc()))
    else:
        print(Fore.RED + f"[ERROR] Can't load model - {str(traceback.format_exc())}")
    exit(1)
print(Fore.GREEN + f"[INFO] Model loaded")
img_worker = Image()
if DEBUG_MODE: print(Fore.YELLOW + f"[INFO] Inited")

init(autoreset=True)

def main(img):
    global data, robot_models
    strt_time = time.time()
     #For windows os !remove!
    #_, img = cap.read()
    cell_robots_coords = {"A": [255, 255],
                            "B": [255, 255],
                            "C": [255, 255],
                            "D": [255, 255]}
    robots_worker = Robots(img)
    robots_count, robots_pixels = robots_worker.robots_count_aruco()
    
    #if DEBUG_MODE: print(Fore.GREEN + f"[DEBUG] Aruco robots count: {robots_count}")
    img, shape = img_worker.corerct_perspective(img)
    img = cv2.resize(img, (512, 512))
    img = img[0:330, 0:512] #убираем пустоту внизу
    if DRAW_VISUAL_ITEMS:
        cv2.line(img, (37, 0), (37, 330), (0, 0, 255), 2)
        cv2.line(img, (512, 0), (512, 330), (0, 0, 255), 2)
    if PROFILER: start_time = time.time()
    img, mask = net.get_colored_img(img)
    if PROFILER: print(Fore.YELLOW + "[PROFILER]Neural Net classification:", time.time() - start_time)
    mask = np.where(mask[0, :, :] == 1, 255, 0)
    cv2.imwrite("mask.png", mask) # исправить
    m = cv2.imread("mask.png") # исправить через np.uint8
    m = cv2.cvtColor(m, cv2.COLOR_RGB2GRAY)
    if DRAW_VISUAL_ITEMS:
        cv2.line(m, (0, 10), (1024, 10), (0, 255, 0))
    contours, hierarchy = cv2.findContours(m,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_TC89_L1)
    moments = [i["m00"] for i in map(cv2.moments, contours)] #площади
    contours = list(contours)
    c = 0
    final = []
    # Новая проверка по площадям
    # Через aruco получаем крлличество роботов
    # Сортируем площади(по убыванию) и минимум равен 
    # n - ому элементу массива площадей 
    temp_moments = sorted(moments, reverse=True)
    min_square = temp_moments[robots_count - 1]
    if min_square < 50: #минимальная площадь слишком маленькая
        print(Fore.YELLOW + "Warning: to minimum. Aruco errored?")
    robots_coords = []
    for i in map(cv2.moments, contours):
        if i["m00"] >= min_square:
            #For coords checking center of robot bottom
            x, y, w, h = cv2.boundingRect(contours[c])
            if DRAW_VISUAL_ITEMS:
                cv2.rectangle(img,(x,y),(x+w,y+h),(0, 255, 0),2)
            coords_detect_x, coords_detect_y = x + w // 2, y + h // 2
            if DRAW_VISUAL_ITEMS:
                cv2.circle(img,(coords_detect_x, coords_detect_y), 7, (0,255,0),-1)

            rect = cv2.minAreaRect(contours[c])
            
            #print(rect[0])
            #cv2.circle(img,(int(rect[0][0]), int(rect[0][1])),5,(0,255,0),-1)
            #center_x = rect[0][0]
            #center_y = rect[0][1]
            box = cv2.boxPoints(rect)
            #cv2.circle(img,(int(box[1][0]), int(box[1][1])),5,(0,255,0),-1)
            #cv2.circle(img,(int(box[2][0]), int(box[2][1])),5,(0,255,0),-1)
            #cv2.circle(img,(int(box[3][0]), int(box[3][1])),5,(0,255,0),-1)
            box = np.int0(box)
            #cv2.circle(img,(box[0][0], box[0][1]),5,(0,255,0),-1)
            if DRAW_VISUAL_ITEMS:
                cv2.drawContours(img,[box],0,(0,0,255),2)
            res = sorted(box.tolist(), key=lambda x: x[1], reverse=1)
            if DRAW_VISUAL_ITEMS:
                cv2.circle(img,(res[0][0], res[0][1]),5,(0,255,0),-1)
                cv2.circle(img,(res[1][0], res[1][1]),5,(0,255,0),-1)
            bottom_x = res[0][0]
            bottom_y = res[0][1]
            bottom_x_1 = res[1][0]
            bottom_y_1 = res[1][1]

            final.append(contours[c])
            robot_id = letters_for_robots[len(final) - 1]
            cntr_color = (255, 255, 255)
            if PROFILER: start_time = time.time()
            for j in robots_pixels:
                x_p = int(j[0] / (1280 / 512) + 16)
                y_p = int(j[1] / (720 / 330) + 20)
                cv2.circle(img, (x_p, y_p), 5, (100, 100, 0), -1)
                
                in_contour = cv2.pointPolygonTest(contours[c], [x_p, y_p], True)
                if in_contour >= 0:
                    #print("Coord:", j)
                    if j[2] == 2:
                        cntr_color = (0, 0, 255)    
                        print(Fore.YELLOW + f"Robot with id {robot_id} is enemy" + Fore.GREEN + "FIRST")
                    elif j[2] == 3:
                        cntr_color = (0, 0, 200)    
                        print(Fore.YELLOW + f"Robot with id {robot_id} is enemy" + Fore.GREEN + "SECOND")
                    elif j[2] == 0:
                        cntr_color = (255, 0, 0)
                        print(Fore.GREEN + f"Robot with id {robot_id} is our" + Fore.GREEN + "FIRST")
                    elif j[2] == 1:
                        cntr_color = (200, 0, 0)
                        print(Fore.GREEN + f"Robot with id {robot_id} is our" + Fore.GREEN + "SECOND")
                    if DRAW_VISUAL_ITEMS:
                        cv2.drawContours(img,[contours[c]],0,cntr_color, -1)
                    
                    break
            if PROFILER: print(Fore.YELLOW + "[PROFILER]Checking robot type(our || enemy):", time.time() - start_time)
            robots_coords += [(bottom_x, bottom_y, robot_id), (bottom_x_1, bottom_y_1, robot_id)]

            #Detect robot on the field usind cells
            if PROFILER: print("Px:", coords_detect_x, coords_detect_y)
            start_time = time.time()
            point = robots_worker.get_cell_by_px((coords_detect_x, coords_detect_y))
            if PROFILER: print(Fore.YELLOW + "[PROFILER]Cell calculating time:", time.time() - start_time)
            #print(f"Robot: {robot_id} coords: {point}")            
            cell_robots_coords[robot_id] = point
            
            
        c += 1
    #Distance checker
    alarms = []
    if PROFILER: start_time = time.time()
    for a, b in itertools.combinations(robots_coords, 2):
        if a[2] != b[2]:
            robot_id_0 = a[2]
            robot_id_1 = b[2]
            a = (a[0], a[1])
            b = (b[0], b[1])
            distance = ((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2) ** 0.5
            if distance <= 60:
                if DRAW_VISUAL_ITEMS:
                    cv2.line(img, a, b, (0, 0, 255), 3)
                if (robot_id_0, robot_id_1) not in alarms and (robot_id_1, robot_id_0) not in alarms:
                    alarms.append((robot_id_0, robot_id_1))
            #if DEBUG_MODE: print(f"Distance between {robot_id_0} and {robot_id_1}: {distance}")
    if PROFILER: print(Fore.YELLOW + "[PROFILER]Distance calcuating time:", time.time() - start_time)
    cell_robots_coords["alarms"] = alarms
    if len(alarms) > 0:
        for i in alarms:
            print(Fore.RED + f"Alarm {i[0]} {i[1]}")
    else:
        print(Fore.GREEN + f"No alarms")
    
    return cell_robots_coords, img
