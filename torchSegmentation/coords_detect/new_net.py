import torch
from torchvision import transforms
import cv2
import numpy as np
import aruco
from colorama import init, Fore
import time, traceback
import itertools

init(autoreset=True)

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
        self.points = np.float32([[254, 656], [766, 655], [283, 394], [741, 397]])
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
            Point Bottom Left((0; 0)) -> ???????????????? ???? ??????????
            Point Top Right -> (1024; 0); 1024 - image width
            Point Bottom Right((1024; 1024)) -> ???????????????? ???? ??????????
        '''
        old_width = image.shape[0]
        old_height = image.shape[1]
        img2 = cv2.resize(image, (512, 288))
        img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
        res = self.concatinate_images(self.img1, img2)
        cv2.imwrite("covered.png", res)
        output_pts = np.float32([[254, 656], [766, 655], [0, 0], [res.shape[1], 0]])
        M = cv2.getPerspectiveTransform(self.points, output_pts)
        out = cv2.warpPerspective(res, M, (res.shape[1], res.shape[0]), flags=cv2.INTER_LINEAR)
        return out, (old_width, old_height)
    def draw_lines(self, image):
        #Border
        cv2.line(image, (0, 0), (0, 512), (0, 255, 0), 3)
        cv2.line(image, (0, 0), (512, 0), (0, 255, 0), 3)
        cv2.line(image, (512, 0), (512, 512), (0, 255, 0), 3)
        #Grid
        for i in range(73, 428, 73):
            cv2.line(image, (i, 0), (i, 330), (0, 255, 0), 3)
        for i in range(55, 314, 55):
            cv2.line(image, (0, i), (512, i), (0, 255, 0), 3)
    def draw_grid_field(self, field):
        #Draw grid on field
        for i in range(151, 605, 151):
            
            cv2.line(field, (0, i), (903, i), (0, 255, 0), 3)
        for i in range(150, 910, 150):
            cv2.line(field, (i, 0), (i, 607), (0, 255, 0), 3)
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
        robots_count = 3 #???? ?????????????????? ???????????????? ???????????? ???? ?????????????????? ?????????????? ?????? ?????????????? (16.jpg)
        return robots_count, self.robots_pixels
    

class Logger:
    def __init__(self, log_path):
        self.log_path = log_path
        with open(log_path, "w") as file:
            file.write("[INFO] Program started")
    def write_log(self, message):
        with open(self.log_path, "a") as file:
            file.write(f"[ERROR][{str(time.ctime())}] {message} \n")
'''
PROD
def only_collisions():
    #initing logger first
    letters_for_robots = ["A", "B", "C", "D", "F", "E"]
    STATUS = 1 #DEBUG - 1; PRODUCTION - 0 #PRODUCTION only errors writing in log file
    if STATUS == 0:
        start_time = time.ctime()
        start_time = str(start_time).replace(":", "-")
        log = Logger(f"logs/{start_time}.txt")
    if STATUS:
        print(Fore.YELLOW + f"[INFO] Testing library mode, running with __name__ == __main__")
        print(Fore.YELLOW + f"[INFO] Loading model...")
    try:
        net = Net("model.t")
    except: 
        if not STATUS: #log
            log.write_log(str(traceback.format_exc()))
        else:
            print(Fore.RED + f"[ERROR] Can't load model - {str(traceback.format_exc())}")
        exit(1)
    print(Fore.GREEN + f"[INFO] Model loaded")
    img_worker = Image()
    
    if STATUS: print(Fore.YELLOW + f"[INFO] Inited")
    for iii in range(10):
        strt_time = time.time()
        img = cv2.imread("tests/13.jpg") #1.jpg 3.jpg 4.jpg(A ?? ?? ???? ???????????? ????????) 5.jpg - ???????????????? ?????????????????? 10.jpg
        
        robots_worker = Robots(img)
        robots_count, robots_pixels = robots_worker.robots_count_aruco()
        if STATUS: print(Fore.GREEN + f"[DEBUG] Aruco robots count: {robots_count}")
        img, shape = img_worker.corerct_perspective(img)
        img = cv2.resize(img, (512, 512))
        img = img[0:330, 0:512] #?????????????? ?????????????? ??????????
        img, mask = net.get_colored_img(img)
        #img_worker.draw_lines(img) #???????????? ?????????? ???? ????????????????????
        mask = np.where(mask[0, :, :] == 1, 255, 0)
        cv2.imwrite("mask.png", mask) # ??????????????????
        m = cv2.imread("mask.png") # ?????????????????? ?????????? np.uint8
        m = cv2.cvtColor(m, cv2.COLOR_RGB2GRAY)
        contours, hierarchy = cv2.findContours(m,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_TC89_L1)
        moments = [i["m00"] for i in map(cv2.moments, contours)] #??????????????
        contours = list(contours)
        c = 0
        final = []
        # ?????????? ???????????????? ???? ????????????????
        # ?????????? aruco ???????????????? ?????????????????????? ??????????????
        # ?????????????????? ??????????????(???? ????????????????) ?? ?????????????? ?????????? 
        # n - ?????? ???????????????? ?????????????? ???????????????? 
        temp_moments = sorted(moments, reverse=True)
        min_square = temp_moments[robots_count - 1]
        if min_square < 50:#?????????????????????? ?????????????? ?????????????? ??????????????????
            print(Fore.YELLOW + "Warning: to minimum. Aruco errored?")
        robots_coords = []
        for i in map(cv2.moments, contours):
            if i["m00"] >= min_square:
                #x,y,w,h = cv2.boundingRect(contours[c])
                #cv2.rectangle(img,(x,y),(x+w,y+h),(0, 255, 0),2)
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
                res = sorted(box.tolist(), key=lambda x: x[1], reverse=1)
                bottom_x = res[0][0]
                bottom_y = res[0][1]
                bottom_x_1 = res[1][0]
                bottom_y_1 = res[1][1]
                #cv2.circle(img,(res[1][1], res[1][0]),5,(0,255,0),-1)

                #print("Bottom coords:", (w // 2 + x, y + h))
                #?????????????????? ?????????? ?????????? ???????????? ?????????????????? ???????? ?????????? ??????????, ???????? ??????????????
                #??????????????????, ???? ???????????????????? ???????? ???????????????????? ???? ????????????(???????? ???????????? ?????????? ???????? )
                #height_under = (y + h) - (((y + h) // 100) * 100) #100 - ???????????? ????????????(????????????????????????)
                #(y + h) // 100 - ?????????? ??????-???? ????????????
                #print(height_under)
                final.append(contours[c])
                robot_id = letters_for_robots[len(final) - 1]
                cx = int(i['m10'] / i['m00'])
                cy = int(i['m01'] / i['m00'])
                for j in robots_pixels:
                    x_p = int(j[0] / 2.5)
                    y_p = int(j[1] / 2.1818 + 20)
                    
                    #cv2.circle(img, (x_p, y_p), 5, (255, 255, 255), -1)
                    #print((x_p, y_p))
                    
                    in_contour = cv2.pointPolygonTest(contours[c], [x_p, y_p], True)
                    if in_contour >= 0:
                        if j[2] == 1:
                            print(Fore.GREEN + f"Robot with id {robot_id} is enemy")
                        else:
                            print(Fore.GREEN + f"Robot with id {robot_id} is our")                        
                        break

                robots_coords += [(bottom_x, bottom_y, robot_id), (bottom_x_1, bottom_y_1, robot_id)]

                #cv2.putText(img, f"{new_coords[0]} {new_coords[1]}", (cx - 20, cy - 15),
                #        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 3)
                #print(f"x: {new_coords[0]} y: {new_coords[1]}")

            c += 1
        
        alarms = []
        
        for a, b in itertools.combinations(robots_coords, 2):
            if a[2] != b[2]:
                robot_id_0 = a[2]
                robot_id_1 = b[2]
                a = (a[0], a[1])
                b = (b[0], b[1])
                distance = ((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2) ** 0.5
                if distance <= 80:
                    if (robot_id_0, robot_id_1) not in alarms and (robot_id_1, robot_id_0) not in alarms:
                        alarms.append((robot_id_0, robot_id_1))
        if len(alarms) > 0:
            for i in alarms:
                print(Fore.RED + f"Alarm {i[0]} {i[1]}")
        else:
            print(Fore.GREEN + f"No alarms")
        print("Time for all operations:", time.time() - strt_time)
    cv2.imshow(f"Res{i}", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
'''

def main():
    #initing logger first
    letters_for_robots = ["A", "B", "C", "D", "F", "E"]
    STATUS = 1 #DEBUG - 1; PRODUCTION - 0 #PRODUCTION only errors writing in log file
    if STATUS == 0:
        start_time = time.ctime()
        start_time = str(start_time).replace(":", "-")
        log = Logger(f"logs/{start_time}.txt")
    if STATUS:
        print(Fore.YELLOW + f"[INFO] Testing library mode, running with __name__ == __main__")
        print(Fore.YELLOW + f"[INFO] Loading model...")
    try:
        net = Net("model.t")
        print(Fore.YELLOW + f"[INFO] yTorch running on {net.DEVICE}")
    except: 
        if not STATUS: #log
            log.write_log(str(traceback.format_exc()))
        else:
            print(Fore.RED + f"[ERROR] Can't load model - {str(traceback.format_exc())}")
        exit(1)
    print(Fore.GREEN + f"[INFO] Model loaded")
    img_worker = Image()
    

    #coords_ranges
    x_0_range = range(0, 113) #vertical 
    x_1_range = range(113, 213)
    x_2_range = range(213, 314)

    y_0_range = range(0, 90) #horizontal
    y_1_range = range(90, 172)
    y_2_range = range(172, 254)
    y_3_range = range(254, 336)
    y_4_range = range(336, 418)
    y_5_range = range(418, 500)
    
    field = cv2.imread("field_lined.jpg")
    if STATUS: print(Fore.YELLOW + f"[INFO] Inited")
    for iii in range(1):
        strt_time = time.time()
        #cap = cv2.VideoCapture(0)
        img = cv2.imread("tests/2.jpg") #1.jpg - ?????? aruco 3.jpg 4.jpg(A ?? ?? ???? ???????????? ????????) 5.jpg - ???????????????? ?????????????????? 10.jpg 13.jpg - ????????; 2 - ?? ??????, ?? ????????
        #_, img = cap.read()
        robots_worker = Robots(img)
        robots_count, robots_pixels = robots_worker.robots_count_aruco()
        if STATUS: print(Fore.GREEN + f"[DEBUG] Aruco robots count: {robots_count}")
        img, shape = img_worker.corerct_perspective(img)
        img = cv2.resize(img, (512, 512))
        img = img[0:330, 0:512] #?????????????? ?????????????? ??????????
        img, mask = net.get_colored_img(img)
        #img_worker.draw_lines(img) #???????????? ?????????? ???? ????????????????????
        mask = np.where(mask[0, :, :] == 1, 255, 0)
        cv2.imwrite("mask.png", mask) # ??????????????????
        m = cv2.imread("mask.png") # ?????????????????? ?????????? np.uint8
        m = cv2.cvtColor(m, cv2.COLOR_RGB2GRAY)
        cv2.line(m, (0, 10), (1024, 10), (0, 255, 0))
        contours, hierarchy = cv2.findContours(m,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_TC89_L1)
        moments = [i["m00"] for i in map(cv2.moments, contours)] #??????????????
        contours = list(contours)
        c = 0
        final = []
        # ?????????? ???????????????? ???? ????????????????
        # ?????????? aruco ???????????????? ?????????????????????? ??????????????
        # ?????????????????? ??????????????(???? ????????????????) ?? ?????????????? ?????????? 
        # n - ?????? ???????????????? ?????????????? ???????????????? 
        temp_moments = sorted(moments, reverse=True)
        min_square = temp_moments[robots_count - 1]
        if min_square < 50:#?????????????????????? ?????????????? ?????????????? ??????????????????
            print(Fore.YELLOW + "Warning: to minimum. Aruco errored?")
        robots_coords = []
        temp_check = []
        for i in map(cv2.moments, contours):
            if i["m00"] >= min_square:
                
                #x,y,w,h = cv2.boundingRect(contours[c])
                #cv2.rectangle(img,(x,y),(x+w,y+h),(0, 255, 0),2)
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
                cv2.drawContours(img,[box],0,(0,0,255),2)
                res = sorted(box.tolist(), key=lambda x: x[1], reverse=1)
                cv2.circle(img,(res[0][0], res[0][1]),5,(0,255,0),-1)
                cv2.circle(img,(res[1][0], res[1][1]),5,(0,255,0),-1)
                bottom_x = res[0][0]
                bottom_y = res[0][1]
                bottom_x_1 = res[1][0]
                bottom_y_1 = res[1][1]
                #cv2.circle(img,(res[1][1], res[1][0]),5,(0,255,0),-1)

                #print("Bottom coords:", (w // 2 + x, y + h))
                #?????????????????? ?????????? ?????????? ???????????? ?????????????????? ???????? ?????????? ??????????, ???????? ??????????????
                #??????????????????, ???? ???????????????????? ???????? ???????????????????? ???? ????????????(???????? ???????????? ?????????? ???????? )
                #height_under = (y + h) - (((y + h) // 100) * 100) #100 - ???????????? ????????????(????????????????????????)
                #(y + h) // 100 - ?????????? ??????-???? ????????????
                #print(height_under)
                final.append(contours[c])
                robot_id = letters_for_robots[len(final) - 1]
                cx = int(i['m10'] / i['m00'])
                cy = int(i['m01'] / i['m00'])
                for j in robots_pixels:
                    x_p = int(j[0] / 2.5)
                    y_p = int(j[1] / 2.1818 + 20)
                    
                    #cv2.circle(img, (x_p, y_p), 5, (255, 255, 255), -1)
                    #print((x_p, y_p))
                    
                    in_contour = cv2.pointPolygonTest(contours[c], [x_p, y_p], True)
                    if in_contour >= 0:
                        if j[2] == 1:
                            cntr_color = (0, 0, 255)    
                            print(Fore.YELLOW + f"Robot with id {robot_id} is enemy")
                        else:
                            cntr_color = (255, 0, 0)
                            print(Fore.GREEN + f"Robot with id {robot_id} is our")
                        cv2.drawContours(img,[contours[c]],0,cntr_color, -1)
                        
                        break
                        
                #print("Centroid:", (cx, cy))
                
                
                pts = [(bottom_x, bottom_y, robot_id), (bottom_x_1, bottom_y_1, robot_id)]

                #old field
                new_coords = [cx, cy]
                robots_coords += pts
                if cy in x_0_range: new_coords[0] = 0
                elif cy in x_1_range: new_coords[0] = 1
                elif cy in x_2_range: new_coords[0] = 2

                if cx in y_0_range: new_coords[1] = 0
                elif cx in y_1_range: new_coords[1] = 1
                elif cx in y_2_range: new_coords[1] = 2
                elif cx in y_3_range: new_coords[1] = 3
                elif cx in y_4_range: new_coords[1] = 4
                elif cx in y_5_range: new_coords[1] = 5

                x_f = (new_coords[0] + 1) * 151 - 75 
                y_f = (new_coords[1] + 1) * 150 - 75 # 75 = 150 / 2
                cv2.circle(field, (y_f, x_f), 50, (0, 0, 255), -1) # Draw robot on field
                
                cv2.putText(img, f"{robot_id}", (cx - 20, cy - 15),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    
                #cv2.putText(img, f"{new_coords[0]} {new_coords[1]}", (cx - 20, cy - 15),
                #        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 3)
                #print(f"x: {new_coords[0]} y: {new_coords[1]}")
            else:
                cv2.drawContours(m, (contours[c]), -1, (0, 0, 0), 3, cv2.FILLED)
                cv2.fillPoly(m, pts = [contours[c]], color=(0,0,0))
                
            c += 1
        start_time = time.time()
        alarms = []
        
        for a, b in itertools.combinations(robots_coords, 2):
            if a[2] != b[2]:
                robot_id_0 = a[2]
                robot_id_1 = b[2]
                a = (a[0], a[1])
                b = (b[0], b[1])
                distance = ((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2) ** 0.5
                if distance <= 80:
                    cv2.line(img, a, b, (0, 0, 255), 3)
                    if (robot_id_0, robot_id_1) not in alarms and (robot_id_1, robot_id_0) not in alarms:
                        alarms.append((robot_id_0, robot_id_1))
                #print(f"Distance between {robot_id_0} and {robot_id_1}: {distance}")
        print(Fore.YELLOW + "Distance calcuating time:", time.time() - start_time)
        if len(alarms) > 0:
            for i in alarms:
                print(Fore.RED + f"Alarm {i[0]} {i[1]}")
        else:
            print(Fore.GREEN + f"No alarms")
        print("FPS for all operations:", 1 / (time.time() - strt_time))
        #m = cv2.cvtColor(m, cv2.COLOR_GRAY2RGB)
        #cv2.drawContours(img, final, -1, (255,0 ,0), 3, cv2.FILLED)
        #cv2.fillPoly(m, final, color=(0,255,0))

        #cv2.imwrite("resulted_mask.png", img)
        #cv2.imwrite("field_with_robots.png", field)
    cv2.imshow(f"Res{i}", img)
    #cv2.imshow(f"Field", field)  
    cv2.waitKey(0)
    cv2.destroyAllWindows()
if __name__ == "__main__":
    main()            
    