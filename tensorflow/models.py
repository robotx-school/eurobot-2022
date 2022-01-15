from typing import Tuple

import tensorflow as tf
import segmentation_models as sm

from config import BACKBONE, NUMBER_CLASSES, OUTPUT_ACTIVATION, INPUT_SHAPE_IMAGE, ENCODER_WEIGHTS, MODEL_NAME


def build_model(backbone_name: str = BACKBONE, num_classes: int = NUMBER_CLASSES, activation: str = OUTPUT_ACTIVATION,
                image_shape: Tuple[int, int, int] = INPUT_SHAPE_IMAGE, encoder_weights: str = ENCODER_WEIGHTS,
                name_model: str = MODEL_NAME) -> tf.keras.models.Model:
    """
    This function builds model based on the input parameters.

    :param backbone_name: name of classification model (without last dense layers) used as feature extractor to
                          build segmentation model.
    :param num_classes: number of classes
    :param activation: name of one of keras.activations for last model layer (e.g. sigmoid, softmax, linear).
    :param image_shape: this is images shape (height, width, channels).
    :param encoder_weights: one of None (random initialization), imagenet (pre-training on ImageNet).
    :param name_model: name model(Unet, Linknet, PSPNet, FPN).
    :return: tf.keras.experimental_model.Model.
    """
    try:
        if name_model == 'Unet':
            model = sm.Unet(backbone_name=backbone_name, encoder_weights=encoder_weights, classes=num_classes,
                            activation=activation, input_shape=image_shape)
        elif name_model == 'Linknet':
            model = sm.Linknet(backbone_name=backbone_name, encoder_weights=encoder_weights, classes=num_classes,
                               activation=activation, input_shape=image_shape)
        elif name_model == 'PSPNet':
            model = sm.PSPNet(backbone_name=backbone_name, encoder_weights=encoder_weights, classes=num_classes,
                              activation=activation, input_shape=image_shape)
        elif name_model == 'FPN':
            model = sm.FPN(backbone_name=backbone_name, encoder_weights=encoder_weights, classes=num_classes,
                           activation=activation, input_shape=image_shape)
        else:
            raise ValueError
    except ValueError:
        raise ValueError('Model name or backbone name or weights name is incorrect')

    return model


if __name__ == '__main__':
    x = build_model(name_model='Unet', backbone_name='resnet18')
    x.summary()
