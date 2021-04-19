import numpy as np
#import pandas as pd
import cv2 as cv
#from google.colab.patches import cv2_imshow # for image display
from skimage import io
#from PIL import Image
import matplotlib.pylab as plt
from math import sqrt




class Vector:
    def __init__(self, vec):
        self.data = vec
        self.x = vec[0]
        self.y = vec[1]
        self.z = vec[2]


class Ommatidium:
    def __init__(self, center, point):
        self.point = point
        self.dir = Vector([point.x - center.x, point.y - center.y, point.z - center.z])  # smerovy vektor
        self.value = [250, 250, 250]


class Eye:
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius
        self.ommatidia = list()

    def get_z(self, x, y):
        temp = self.radius ** 2 - (x - self.center.x) ** 2 - (y - self.center.y) ** 2
        if temp >= 0:
            return sqrt(temp)
        else:
            return -sqrt(abs(temp))

    def in_circle(self, x, y):
        return True if (((x - self.center.x) ** 2 - (y - self.center.y) ** 2) <= self.radius ** 2) else False

    def get_ommatidia(self, num):
        # Hranice oka v rovine XY
        min_x = self.center.x - self.radius
        max_x = self.center.x + self.radius
        min_y = self.center.y - self.radius
        max_y = self.center.y + self.radius

        # Startovni souradnice
        x = min_x
        y = min_y

        # Krok - o kolik se lisi vzdalenosti dvou ommatidii
        step = (max_x - min_x) / sqrt(num)

        # hranice pro vypocet, abychom dosahli +- spravneho poctu
        border = int(sqrt(num) // 2)

        for xx in range(-border, +border):
            y = min_y
            x += step
            for yy in range(-border, +border):
                y += step
                if not self.in_circle(x, y):
                    continue
                z = self.get_z(x, y)
                if z >= 0:
                    self.ommatidia.append(Ommatidium(self.center, Vector([x, y, z])))

if __name__ == "__main__":

    url = "/content/wp2116405.jpg"
    image = io.imread(url)

    # Z nejakeho duvodu je defaultni format obskurni BGR. Prevedeme si ho do standardniho RGB a zobrazime obrazek.
    image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    cv2_imshow(image)

    new_image = np.ndarray(image.shape).astype(np.float32)
    for r in range(image.shape[0]):
        for c in range(image.shape[1]):
            px = image[r, c]
            new_image[r, c] = [int(px[0] / 3), px[1], int(px[2] * 1.5)]

    image = cv.cvtColor(new_image, cv.COLOR_BGR2RGB)

    # cv2_imshow(new_image)

    resolution = 100  # dpi = 4 px/mm
    z0 = 50  # mm
    r = 1.5  # polomer oka
    d = 6  # vzdalenost stredu oci
    rows = image.shape[0]
    cols = image.shape[1]
    num_omm = 9000