import time
import net
import cv2

IMAGE_RECIEVE_MODE = 0 #0 - local file; 1 - camera;
if IMAGE_RECIEVE_MODE == 1:
    cap = cv2.VideoCapture(0)
while True:
    if IMAGE_RECIEVE_MODE == 0:
        image = cv2.imread("tests/3.jpg")
    elif IMAGE_RECIEVE_MODE == 1:
        ret, image = cap.read()
    strt_time = time.time()    
    data, img = net.main(image)
    print("FPS:", 1 / (time.time() - strt_time))
    print(data)
    cv2.imshow("Detected", img)
    k = cv2.waitKey(1)
    if k == 27:
        cv2.destroyAllWindows()
        if IMAGE_RECIEVE_MODE == 1:
            cap.release()
        break