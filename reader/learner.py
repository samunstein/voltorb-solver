import keras
from sklearn.model_selection import train_test_split
import numpy as np
import scipy.misc
import os
import keras.utils

import reader


import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Conv2D, MaxPooling2D

batch_size = 64
epochs = 100

VOLTORBS = (2, 6)
FIRST = (0, 2)
SECOND = (1, 10)


def read_images(which):
    f = open("labels.txt")
    data = []
    labels = []
    place, classes = which
    for line in f:
        parts = line.strip().split(":")
        numbers = parts[1].split(" ")
        img = scipy.misc.imread(parts[0])
        data.append(img)
        labels.append(keras.utils.to_categorical(int(numbers[place]), classes).reshape(classes))
    f.close()

    return np.array(data), np.array(labels)


def train(which, debug=True):
    num_classes = which[1]
    x, y = read_images(which)
    if debug:
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.10)
        print('x_train shape:', x_train.shape)
        print(x_train.shape[0], 'train samples')
        print(x_test.shape[0], 'test samples')
    else:
        x_train, y_train = x, y

    model = Sequential()

    model.add(Conv2D(64, (3, 3), padding='same', input_shape=x_train.shape[1:]))
    model.add(Activation('tanh'))
    model.add(Conv2D(64, (3, 3)))
    model.add(Activation('tanh'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Conv2D(64, (3, 3), padding='same'))
    model.add(Activation('tanh'))
    model.add(Conv2D(64, (3, 3)))
    model.add(Activation('tanh'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Conv2D(64, (3, 3), padding='same'))
    model.add(Activation('tanh'))
    model.add(Conv2D(64, (3, 3)))
    model.add(Activation('tanh'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Conv2D(64, (3, 3), padding='same'))
    model.add(Activation('tanh'))
    model.add(Conv2D(64, (3, 3)))
    model.add(Activation('tanh'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Flatten())
    model.add(Dense(512))
    model.add(Activation('tanh'))
    model.add(Dropout(0.5))
    model.add(Dense(num_classes))
    model.add(Activation('softmax'))

    # initiate RMSprop optimizer
    opt = keras.optimizers.rmsprop(lr=0.0001, decay=1e-6)

    # Let's train the model using RMSprop
    model.compile(loss='categorical_crossentropy',
                  optimizer=opt,
                  metrics=['accuracy'])

    if debug:
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

    else:
        model.fit(x_train, y_train,
                  batch_size=batch_size,
                  epochs=epochs,
                  shuffle=True)

        return model




def augment(place, number):
    f = open("labels.txt")
    images = []
    labels = []
    for line in f:
        parts = line.strip().split(":")
        numbers = parts[1].split(" ")
        if int(numbers[place]) == number:
            img = scipy.misc.imread(parts[0])
            images.append(img)
            labels.append(parts[1])

    newimgs = []
    for i in range(len(images)):
        img = images[i]
        newimgs.append(np.roll(img, 5, 1))
        newimgs.append(np.roll(img, -5, 1))
        newimgs.append(np.roll(img, -5, 0))
        newimgs.append(np.roll(img, 5, 0))

    count = reader.count_images()
    file = open("labels.txt")
    lines = file.read().split("\n")
    file.close()
    for i in range(count, count + len(newimgs)):
        scipy.misc.imsave("img/h{}.png".format(i), newimgs[i - count])
        hintstr = labels[(i - count) // 4]
        lines.append("../reader/img/h{}.png".format(i) + ":" + hintstr)
    file = open("labels.txt", "w")
    file.write("\n".join(lines))
    file.close()


def main():
    #augment(1, 9)
    model = train(FIRST, debug=False)
    model.save("first.h5")


if __name__ == "__main__":
    main()
