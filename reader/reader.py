import pygame.camera
import pygame.image
import sys
import pygame.surfarray
import scipy.misc
import os
from PIL import Image

IMGHEIGHT = 480
IMGWIDTH = 640

READERFOLDER = "./"


def getslice(imag, cx, cy):
    s = 86

    startx = int(cx - s/2) if cx + s/2 < IMGWIDTH else IMGWIDTH - s
    starty = int(cy - s/2) if cy + s/2 < IMGHEIGHT else IMGHEIGHT - s

    return imag[startx:startx+s, starty:starty+s, :]


def imgprocess(imag):
    start = (16, 9)
    size = 470
    size6 = size / 6
    centers = [[(start[0] + (i + 0.5) * size6, start[1] + (j + 0.5) * size6) for i in range(6)] for j in range(6)]

    imgs = [[getslice(imag, *center) for center in lists] for lists in centers]

    return imgs


def read_webcam():
    pygame.camera.init()

    cameras = pygame.camera.list_cameras()
    webcam = pygame.camera.Camera(cameras[0])
    webcam.start()

    # grab first frame
    img = webcam.get_image()

    WIDTH = img.get_width()
    HEIGHT = img.get_height()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("pyGame Camera View")

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                nparr = pygame.surfarray.array3d(img)
                return nparr

        # draw frame
        screen.blit(img, (0, 0))
        pygame.display.flip()
        # grab next frame
        img = webcam.get_image()


def read_file():
    img = scipy.misc.imread(READERFOLDER + "out.png")
    return img


def save_hints(hints, numbers):
    if len(numbers) > 20:
        print("There has to be 20 hints")
        return
    count = count_images()
    file = open(READERFOLDER + "labels.txt")
    lines = file.read().split("\n")
    for i in range(count, count + 10):
        scipy.misc.imsave(READERFOLDER + "img/h{}.png".format(i), hints[i - count].transpose(1, 0, 2))
        lines.append(READERFOLDER + "img/h{}.png".format(i) + ":" + " ".join(numbers[2*(i - count):2*(i - count + 1)]))
    file.close()
    file = open(READERFOLDER + "labels.txt", "w")
    file.write("\n".join(lines))
    file.close()


def hints(imgs):
    hintlist = []
    for i in range(5):
        hintlist.append(imgs[i][5])
    for i in range(5):
        hintlist.append(imgs[5][i])
    return hintlist


def count_images():
    return len(os.listdir(READERFOLDER + "img"))


def label_images():
    labels = []
    for name in os.listdir(READERFOLDER + "img"):
        img = scipy.misc.imread(os.path.join(READERFOLDER + "img", name))
        img = Image.fromarray(img, 'RGB')
        img.show()
        labels.append(name + ":" + input())
    print("\n".join(labels))


def read_webcam_and_save_hints():
    img = read_webcam()
    hintnumbers = input()
    imgs = imgprocess(img)
    hint = hints(imgs)
    save_hints(hint, hintnumbers)

if __name__ == "__main__":
    read_webcam()