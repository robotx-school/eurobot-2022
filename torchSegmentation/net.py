import torch
from torchvision import transforms
import cv2
import numpy as np
import aruco

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
            Point Bottom Left((0; 0)) -> (0; 0)
            Point Top Right -> (1024; 0); 1024 - image width
            Point Bottom Right((1024; 1024)) -> (1024; 1024)
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
    def draw_lines(self, image):
        #Border
        cv2.line(image, (0, 0), (0, 512), (0, 255, 0), 3)
        cv2.line(image, (0, 0), (512, 0), (0, 255, 0), 3)
        cv2.line(image, (512, 0), (512, 512), (0, 255, 0), 3)
        #Grid
        for i in range(90, 428, 82):
            cv2.line(image, (i, 0), (i, 330), (0, 255, 0), 3)
        for i in range(113, 314, 100):
            cv2.line(image, (0, i), (512, i), (0, 255, 0), 3)
    def draw_grid_field(self, field):
        #Draw grid on field
        for i in range(151, 605, 151):
            cv2.line(field, (0, i), (903, i), (0, 255, 0), 3)
        for i in range(150, 910, 150):
            cv2.line(field, (i, 0), (i, 607), (0, 255, 0), 3)
class Robots:
    def __init__(self, img):
        self.aruco_data = aruco.find_robots(img)
        self.img = img
    def recheck_aruco(self, img):
        self.aruco_data = aruco.find_robots(img)
        self.img = img
    def robots_count_aruco(self):
        robots_count = 0
        for i in self.aruco_data:
            if i[0] != 255 or i[1] != 255:
                robots_count += 1
        robots_count = 4 #на имеющихся тестовых данных на некоторых роботах нет маркера (16.jpg)
        return robots_count

if __name__ == "__main__":
    
    print("Testing library")
    print("Loading model...")
    net = Net("model.t")
    print("Model loaded")
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
    print("Inited")
    
    img = cv2.imread("tests/7.jpg")
    field = cv2.imread("field_lined.jpg")
    robots_worker = Robots(img)
    robots_count = robots_worker.robots_count_aruco()
    print(robots_count)

    
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img, shape = img_worker.corerct_perspective(img)
    img = cv2.resize(img, (512, 512))
    img = img[0:330, 0:512] #убираем пустоту внизу
    img, mask = net.get_colored_img(img)
    img_worker.draw_lines(img) #рисуем сетку на фотографии
    mask = np.where(mask[0, :, :] == 1, 255, 0)
    cv2.imwrite("mask.png", mask) # исправить
    m = cv2.imread("mask.png") # исправить через np.uint8
    m = cv2.cvtColor(m, cv2.COLOR_RGB2GRAY)
    cv2.line(m, (0, 10), (1024, 10), (0, 255, 0))

    contours, hierarchy = cv2.findContours(m,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_TC89_L1)
    mm = cv2.moments
    mm = list(map(cv2.moments, contours))
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
    for i in map(cv2.moments, contours):
        if i["m00"] >= min_square:
            final.append(contours[c])
            cx = int(i['m10']/i['m00'])
            cy = int(i['m01']/i['m00'])
            new_coords = [cx, cy]

            if cy in x_0_range: new_coords[0] = 0
            elif cy in x_1_range: new_coords[0] = 1
            elif cy in x_2_range: new_coords[0] = 2

            if cx in y_0_range: new_coords[1] = 0
            elif cx in y_1_range: new_coords[1] = 1
            elif cx in y_2_range: new_coords[1] = 2
            elif cx in y_3_range: new_coords[1] = 3
            elif cx in y_4_range: new_coords[1] = 4
            elif cx in y_5_range: new_coords[1] = 5

            #Draw cicle on the field
            x_f = (new_coords[0] + 1) * 151 - 75 
            y_f = (new_coords[1] + 1) * 150 - 75 # 75 = 150 / 2
            print(y_f)
            cv2.circle(field, (y_f, x_f), 50, (0, 0, 255), -1) #Draw robot on field
            cv2.putText(img, f"{new_coords[0]} {new_coords[1]}", (cx - 20, cy - 15),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 3)
            print(f"x: {new_coords[0]} y: {new_coords[1]}")
            
        else:
            cv2.drawContours(m, (contours[c]), -1, (0, 0, 0), 3, cv2.FILLED)
            cv2.fillPoly(m, pts = [contours[c]], color=(0,0,0))

        c += 1

    m = cv2.cvtColor(m, cv2.COLOR_GRAY2RGB)
    cv2.drawContours(img, final, -1, (255,0 ,0), 3, cv2.FILLED)
    cv2.fillPoly(m, final, color=(0,255,0))

    cv2.imwrite("resulted_mask.png", img)
    cv2.imwrite("field_with_robots.png", field)
    cv2.imshow(f"Res{i}", img)
    cv2.imshow(f"Field", field)
cv2.waitKey(0)
cv2.destroyAllWindows()
            
