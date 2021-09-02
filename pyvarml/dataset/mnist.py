# Copyright 2021 Variscite LTD
# SPDX-License-Identifier: BSD-3-Clause

import numpy as np
import matplotlib.pyplot as plt

import tensorflow as tf
assert float(tf.__version__[:3]) >= 2.4
from tensorflow import keras

def version():
    print("version")

def retrieve_mnist_model():
    print("get mnist trained model from variscite FTP")

def get_available_mnist_models():
    print("returns available mnist models from FTP")

def train_mnist_digit():
    print("aaa")
    mnist = keras.datasets.mnist
    (train_images, train_labels), (test_images, test_labels) = mnist.load_data()

    train_images = train_images / 255.0
    test_images = test_images / 255.0
                
    model = keras.Sequential([
        keras.layers.Flatten(input_shape=(28, 28)),
        keras.layers.Dense(128, activation=tf.nn.relu),
        keras.layers.Dense(10)
    ])

    model.compile(optimizer='adam',
                  loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                  metrics=['accuracy'])
                  
    model.fit(train_images, train_labels, epochs=5)     

    test_loss, test_acc = model.evaluate(test_images, test_labels)

    print('Test accuracy:', test_acc)   

    predictions = model.predict(test_images)

    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    tflite_model = converter.convert()

    return tflite_model, test_loss, test_acc
    
    
