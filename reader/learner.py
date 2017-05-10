import keras
from sklearn.model_selection import train_test_split
import numpy as np
import scipy.misc
import os

import keras
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Conv2D, MaxPooling2D

batch_size = 32
num_classes = 16+6
epochs = 50

def transform_label(val, values):
    return [1 if i == val else 0 for i in range(values)]


def read_images():
    f = open("labels.txt")
    data = []
    labels = []
    for line in f:
        parts = line.strip().split(":")
        numbers = parts[1].split(" ")
        label = []
        label.extend(transform_label(int(numbers[2]), 6))

        img = scipy.misc.imread(os.path.join("img", parts[0]))
        if img.shape == (86, 86, 3):
            data.append(img)
            labels.append(label)

    return np.array(data), labels


def train():
    x, y = read_images()
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.10)

    print('x_train shape:', x_train.shape)
    print(x_train.shape[0], 'train samples')
    print(x_test.shape[0], 'test samples')

    model = Sequential()

    model.add(Conv2D(32, (4, 4), padding='same', input_shape=x_train.shape[1:]))
    model.add(Activation('softmax'))
    model.add(Conv2D(32, (4, 4)))
    model.add(Activation('softmax'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Conv2D(64, (4, 4), padding='same'))
    model.add(Activation('softmax'))
    model.add(Conv2D(64, (4, 4)))
    model.add(Activation('softmax'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Flatten())
    model.add(Dense(100))
    model.add(Activation('softmax'))
    model.add(Dropout(0.5))
    model.add(Dense(num_classes))
    model.add(Activation('softmax'))

    # initiate RMSprop optimizer
    opt = keras.optimizers.rmsprop(lr=0.0001, decay=1e-6)

    # Let's train the model using RMSprop
    model.compile(loss='categorical_crossentropy',
                  optimizer=opt,
                  metrics=['accuracy'])

    model.fit(x_train, y_train,
              batch_size=batch_size,
              epochs=epochs,
              validation_data=(x_test, y_test),
              shuffle=True)

train()