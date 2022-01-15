import os
import json
from typing import Tuple

import cv2
import numpy as np
import albumentations as A
from tensorflow import keras


from ..config import BATCH_SIZE, INPUT_SHAPE_IMAGE, JSON_FILE_NAME, NUMBER_CLASSES, AUGMENTATION_DATA


class DataGenerator(keras.utils.Sequence):
    def __init__(self, data_path: str, batch_size: int = BATCH_SIZE, json_name: str = JSON_FILE_NAME,
                 image_shape: Tuple[int, int, int] = INPUT_SHAPE_IMAGE, is_train: bool = True,
                 num_classes: int = NUMBER_CLASSES, augmentation_data: bool = AUGMENTATION_DATA) -> None:
        """
        Data generator for the task of semantic segmentation.

        :param batch_size: number of images in one batch.
        :param image_shape: this is images shape (height, width, channels).
        :param is_train: if is_train = True, then we work with train images, otherwise with test.
        :param json_name: this is name json file.
        :param num_classes: number of classes.
        :param augmentation_data: if this parameter is True, then augmentation is applied to the training dataset.
        """

        self.batch_size = batch_size
        self.image_shape = image_shape
        self.num_classes = num_classes
        self.is_train = is_train

        # read json
        with open('data/data.json') as f:
            self.data = json.load(f)

        # augmentation data
        if self.is_train:
            self.data = self.data['train']
            augmentation = self.augmentation_images(augmentation_data)
        else:
            self.data = self.data['test']
            augmentation = self.augmentation_images()

        self.aug = augmentation
        self.on_epoch_end()

    def on_epoch_end(self) -> None:
        """
        Random shuffling of data at the end of each epoch.

        """
        np.random.shuffle(self.data)

    def __len__(self) -> int:
        return len(self.data) // self.batch_size + (len(self.data) % self.batch_size != 0)

    def __getitem__(self, batch_idx: int) -> Tuple[np.ndarray, np.ndarray]:
        """
        This function makes batch.

        :param batch_idx: batch number.
        :return: images tensor and list with labels tensors for each output.
        """
        batch = self.data[(batch_idx * self.batch_size):((batch_idx + 1) * self.batch_size)]
        images = np.zeros((self.batch_size, self.image_shape[0], self.image_shape[1], self.image_shape[2]))
        masks = np.zeros((self.batch_size, self.image_shape[0], self.image_shape[1], self.num_classes))
        for i, image_dict in enumerate(batch):
            img = cv2.imread(image_dict['image_path'])
            # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            mask_image = cv2.imread(image_dict['mask_path'], 0)
            # cv2.imshow('mask', mask_image)
            # cv2.imshow('image', img)
            # cv2.waitKey(0)
            augmented = self.aug(image=img, mask=mask_image)
            img = augmented['image']
            mask_image = augmented['mask']
            images[i, :, :, :] = img
            masks[i, :, :, 0] = np.where(mask_image == 20, 1, 0)  # robot
            masks[i, :, :, -1] = np.where(mask_image == 0, 1, 0)  # background
        images = image_normalization(images)
        return images, masks

    def augmentation_images(self, augm: bool = False) -> A.Compose:
        """
        This function makes augmentation data.

        :return: augment data
        """
        if augm is True:
            aug = A.Compose([
                A.Resize(height=self.image_shape[0], width=self.image_shape[1]),
                A.Blur(blur_limit=4, p=0.3),
                A.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.0, hue=0.0, always_apply=False, p=0.2),
                A.GaussNoise(var_limit=(10.0, 50.0), mean=0, always_apply=False, p=0.4),
                A.HueSaturationValue(hue_shift_limit=5, sat_shift_limit=5, val_shift_limit=5, always_apply=True,
                                     p=0.2)
            ])
        else:
            aug = A.Compose([A.Resize(height=self.image_shape[0], width=self.image_shape[1])])

        return aug


def image_normalization(image: np.ndarray) -> np.ndarray:
    """
    Image normalization.
    :param image: images numpy array.
    :return: normalized images.
    """
    return image / 255.0

