import keras
from sklearn.model_selection import train_test_split
import numpy as np
import scipy.misc
import os
import keras.utils


import keras
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Conv2D, MaxPooling2D

batch_size = 32
num_classes = 6
epochs = 5


def read_images():
    f = open("labels.txt")
    data = []
    labels = []
    for line in f:
        parts = line.strip().split(":")
        numbers = parts[1].split(" ")
        img = scipy.misc.imread(parts[0])
        data.append(img)
        labels.append(keras.utils.to_categorical(int(numbers[1]), 6).reshape(6))

    return np.array(data), np.array(labels)


def train():
    x, y = read_images()
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.10)

    print('x_train shape:', x_train.shape)
    print(x_train.shape[0], 'train samples')
    print(x_test.shape[0], 'test samples')

    model = Sequential()

    model.add(Conv2D(16, (2, 2), padding='same', input_shape=x_train.shape[1:]))
    model.add(Activation('tanh'))
    model.add(Conv2D(16, (2, 2)))
    model.add(Activation('tanh'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Conv2D(32, (3, 3), padding='same'))
    model.add(Activation('tanh'))
    model.add(Conv2D(32, (3, 3)))
    model.add(Activation('tanh'))
    model.add(Conv2D(32, (3, 3), padding='same'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Flatten())
    model.add(Dense(128))
    model.add(Activation('tanh'))
    model.add(Dropout(0.25))
    model.add(Dense(num_classes))
    model.add(Activation('softmax'))

    model.compile(loss='mean_squared_error', optimizer='sgd', metrics=['accuracy'])

    model.fit(x_train, y_train,
              batch_size=batch_size,
              epochs=epochs,
              validation_data=(x_test, y_test),
              shuffle=True)

    y = model.predict(x_test)
    predicted = np.argmax(y, 1)
    real = np.argmax(y_test, 1)

    print("Predicted: ")
    print(predicted)
    print("Real: ")
    print(real)

    print("Accuracy: ")
    acc = [1 if predicted[i] == real[i] else 0 for i in range(predicted.shape[0])]
    print(sum(acc) / len(acc))

train()