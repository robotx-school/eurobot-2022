import time
import argparse

import cv2
import numpy as np
import tensorflow as tf
import segmentation_models as sm
import matplotlib.pyplot as plt
from tqdm import tqdm

from config import INPUT_SHAPE_IMAGE
from src import DataGenerator, build_model

sm.set_framework('tf.keras')
sm.framework()

def preparing_frame(image: np.ndarray, model) -> np.ndarray:
    """
    This function prepares the images and makes a prediction.

    :param image: this is input images or frame.
    :param model: assembled model with loaded weights.
    :return: images with an overlay masks
    """

    image = cv2.resize(image, (INPUT_SHAPE_IMAGE[1], INPUT_SHAPE_IMAGE[0]))
    mask = model.predict(np.expand_dims(image, axis=0) / 255.0)[0]
    mask = np.where(mask >= 0.5, 1, 0)

    image[:, :, 0] = np.where(mask[:, :, 0] == 1, 0, image[:, :, 0])
    image[:, :, 1] = np.where(mask[:, :, 0] == 1, 0, image[:, :, 1])
    image[:, :, 2] = np.where(mask[:, :, 0] == 1, 0, image[:, :, 2])
    image[:, :, 0] = np.where(mask[:, :, 0] == 1, 255, image[:, :, 0])
    image[:, :, 2] = np.where(mask[:, :, 0] == 1, 255, image[:, :, 2])



    return image, mask


def visualization(weights: str, path_video: str) -> None:
    """
    This function captures video and resizes the images.
    """
    model = build_model()
    model.load_weights(weights)

    cap = cv2.VideoCapture(path_video)

    if not cap.isOpened():
        print("Error opening video stream or file")

    prev_frame_time = 0

    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            break

        cv2.resize(frame, (INPUT_SHAPE_IMAGE[1], INPUT_SHAPE_IMAGE[0]))
        image = preparing_frame(image=frame, model=model)
        image = cv2.resize(image, (720, 720))
        new_frame_time = time.time()
        fps = 1 / (new_frame_time - prev_frame_time)
        prev_frame_time = new_frame_time
        cv2.putText(image, str(int(fps)) + ':fps', (150, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
        cv2.imshow('frame', image)
        if cv2.waitKey(1) == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()


def show_batch(data_path: str):
    """
    This function shows images and masks.
    """
    data_show = DataGenerator('/home/andre/pycharm/lety/data/')

    for i in range(len(data_show)):
        batch = data_show[i]

        images, masks = batch[0], batch[1]
        fontsize = 8
        for n, j in enumerate(images):
            cv2.imshow('img', np.uint8(j * 255))
            cv2.imshow('road', np.uint8(np.where(masks[n, :, :, 0] > 0, 255, 0)))
            cv2.imshow('white line', np.uint8(np.where(masks[n, :, :, 1] > 0, 255, 0)))
            cv2.imshow('yellow line', np.uint8(np.where(masks[n, :, :, 2] > 0, 255, 0)))
            cv2.imshow('red line', np.uint8(np.where(masks[n, :, :, 3] > 0, 255, 0)))
            cv2.imshow('background', np.uint8(np.where(masks[n, :, :, -1] > 0, 255, 0)))
            cv2.waitKey(0)


def test_metrics_and_time(mode: str) -> None:
    """
    This function calculates the average value of loss and metrics as well as inference time and average fps.

    :param mode: depending on the mode ('metrics', 'time'), the function counts (loss, metrics) or time and average fps.
    """
    data_gen = DataGenerator(data_path=args.data_path, batch_size=1, json_name=args.json_name, is_train=False)
    model = build_model()
    # model = EffCustom_2().build_eff()
    # model = build_model()
    model.load_weights(args.weights)
    model.compile(loss=tf.keras.losses.binary_crossentropy, metrics=[
        'accuracy', sm.metrics.iou_score, sm.metrics.precision, sm.metrics.recall, sm.metrics.f1_score
    ])

    if mode == 'metrics':
        print(model.evaluate(data_gen, workers=8))

    elif mode == 'time':
        all_times = []
        for i in tqdm(range(len(data_gen))):
            images, _ = data_gen[i]
            start_time = time.time()
            model.predict(images)
            finish_time = time.time()
            all_times.append(finish_time - start_time)
        all_times = all_times[5:]
        message = '\nMean inference time: {:.04f}. Mean FPS: {:.04f}.\n'.format(
            np.mean(all_times),
            len(all_times) / sum(all_times))
        print(message)


def parse_args() -> argparse.Namespace:
    """
    Parsing command line arguments with argparse.
    """
    parser = argparse.ArgumentParser('script for model testing.')
    parser.add_argument('--weights', type=str, default=None, help='Path for loading model weights.')
    parser.add_argument('--path_video', type=str, default=None, help='Path for loading video for test.')
    parser.add_argument('--metrics', action='store_true', help='If the value is True, then the average '
                                                               'metrics on the validation dataset will be calculated.')
    parser.add_argument('--time', action='store_true', help='If the value is True, then the inference time and the '
                                                            'average fps on the validation dataset will be calculated.')
    parser.add_argument('--gpu', type=str, default='_', help='If you want to use the GPU, you must specify the number '
                                                             'of the video card that you want to use.')
    parser.add_argument('--data_path', type=str, default='data/first_data',
                        help='path to Dataset where there is a json file')
    parser.add_argument('--json_name', type=str, default='data.json', help='path to Dataset where there is a json file')
    parser.add_argument('--batch', action='store_true', help='If True, the screen will display batches '
                                                             'from data_generator.')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()

    if args.gpu != '_':
        gpus_list = [int(args.gpu)]
    else:
        gpus_list = []
    devices = tf.config.get_visible_devices('GPU')
    devices = [devices[i] for i in gpus_list]
    tf.config.set_visible_devices(devices, 'GPU')
    for gpu in devices:
        tf.config.experimental.set_memory_growth(gpu, True)

    if args.path_video is not None:
        visualization(weights=args.weights, path_video=args.path_video)
    if args.metrics:
        test_metrics_and_time('metrics')
    if args.time:
        test_metrics_and_time('time')
    if args.batch:
        show_batch(args.data_path)

model = build_model()
model.load_weights("Unetresnet18.h5")
img = cv2.imread('test_image.jpg')
# img_detect = img[img.shape[0]//2:]
img_masked, mask = preparing_frame(image=img, model=model)
mask = np.where(mask[:, :, 0] == 1, 255, 0)
cv2.imwrite("mask.png", mask)
m = cv2.imread("mask.png")
m = cv2.cvtColor(m, cv2.COLOR_RGB2GRAY)
contours, hierarchy = cv2.findContours(m,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_TC89_L1)
mm = cv2.moments
mm = list(map(cv2.moments, contours))
moments = [i["m00"] for i in map(cv2.moments, contours)]
contours = list(contours)
c = 0
final = []
for i in map(cv2.moments, contours):
    if i["m00"] >= 400:
        final.append(contours[c])
    else:
        cv2.drawContours(m, contours[c], -1, (0, 0, 0), 3, cv2.FILLED)
        cv2.fillPoly(m, pts =[contours[c]], color=(0,0,0))

    c += 1

m = cv2.cvtColor(m, cv2.COLOR_GRAY2RGB)
cv2.drawContours(m, final, -1, (0, 255,0), 3, cv2.FILLED)
cv2.fillPoly(m, final, color=(0,255,0))
cv2.imwrite("resulted_mask.png", m)
img_masked = cv2.resize(img_masked, (img.shape[1], img.shape[0]))
result = np.hstack((img, img_masked))
cv2.imwrite('result.jpg', result)
