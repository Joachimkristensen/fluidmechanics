import math
import numpy as np
from colors import ColorThing
from PIL import Image

PIXEL_SIZE = 0.62
X_DIFF = 382
Y_DIFF = 326
X_SIZE = 167
Y_SIZE = 150


class Interpolator():
    def __init__(self, file_name, output_file):
        self.output_file = output_file
        self.input_file = open(file_name, "r")
        self.x_size = math.ceil(X_DIFF)
        self.y_size = math.ceil(Y_DIFF)
        self.img = np.zeros([self.x_size, self.y_size], dtype=object)
        self.content = self.input_file.readlines()

        self.interpolate_list = []
        self.x_prev = 0
        self.y_prev = 0
        self.y_i = 0
        self.x_i = 0
        self.i = 0
        self.x_offsets = np.zeros(X_SIZE, dtype=int)

    def get_reference_point(self, flag):
        line = self.content[0].split(' ')
        self.y_prev = float(line[1])

        if flag:
            self.x_prev = float(self.content[0].split(' ')[0])
            v_m = float(line[2])
            self.img[self.x_i, self.y_i] = v_m

    def interpolate_points(self):
        self.get_reference_point(True)
        self.interpolate_column(0, self.x_offsets[0])
        self.interpolate_row()

        for i in range(1, X_SIZE + 1):
            self.get_reference_point(False)
            self.interpolate_column(i, self.x_offsets[i - 1] + 1)

        self.interpolate_offsets()
        self.save()

    def interpolate_offsets(self):
        for self.y_i in range(1, Y_DIFF):
            self.x_i = 0
            for offset in self.x_offsets:
                if offset != 0:
                    for i in range(offset):
                        self.interpolate_list.append(
                            (self.x_i + i + 1, self.y_i))

                    self.interpolate_colour(
                        (self.x_i, self.y_i), (self.x_i + offset + 1, self.y_i))
                self.x_i += offset + 1

    def interpolate_colour(self, v1, v2):
        discount = abs(self.img[v1] - self.img[v2]) / \
            (len(self.interpolate_list) + 1)

        if self.img[v1] > self.img[v2]:
            for i in range(len(self.interpolate_list)):
                self.img[self.interpolate_list[i]
                         ] = self.img[v1] - discount * (i + 1)

        else:
            for i in range(len(self.interpolate_list)):
                self.img[self.interpolate_list[i]
                         ] = self.img[v1] + discount * (i + 1)

        self.interpolate_list.clear()

    def interpolate_row(self):
        for x in range(Y_SIZE, len(self.content), Y_SIZE):
            line = self.content[x].split(' ')
            _x = float(line[0])
            v_m = float(line[2])

            offsets = 0

            while self.x_prev < _x:
                self.x_prev += PIXEL_SIZE
                offsets += 1
                self.x_i += 1
                self.interpolate_list.append((self.x_i, self.y_i))

            self.img[self.x_i, self.y_i] = v_m

            if len(self.interpolate_list) > 1:
                self.interpolate_list.remove(self.interpolate_list[-1])
                v1 = (self.interpolate_list[0][0] - 1, self.y_i)
                v2 = (self.interpolate_list[-1][0] + 1, self.y_i)
                self.interpolate_colour(v1, v2)

            self.x_offsets[self.i] = offsets - 1
            _x -= _x - self.x_prev
            self.x_prev = _x
            self.i += 1

        self.x_i = 0
        self.i = 0

    def interpolate_column(self, i, offset):
        self.x_i += offset

        for y in range(2 + Y_SIZE * i, (2 + Y_SIZE * i) + Y_SIZE - 2):
            line = self.content[y].split(' ')
            _y = float(line[1])
            v_m = float(line[2])

            while self.y_prev < _y:
                self.y_prev += PIXEL_SIZE
                self.y_i += 1
                self.interpolate_list.append((self.x_i, self.y_i))

            self.img[self.x_i, self.y_i] = v_m

            if len(self.interpolate_list) > 1:
                self.interpolate_list.remove(self.interpolate_list[-1])
                v1 = (self.x_i, self.interpolate_list[0][1] - 1)
                v2 = (self.x_i, self.interpolate_list[-1][1] + 1)
                self.interpolate_colour(v1, v2)

            _y -= _y - self.y_prev
            self.y_prev = _y

            self.i += 1

        self.y_i = 0
        self.i = 0

    def save(self):
        color_thing = ColorThing()

        for x in range(self.x_size):
            for y in range(self.y_size):
                c = (color_thing.v_interval(self.img[x, y]))
                self.img[x, y] = np.asarray(c, dtype=np.uint8)

        img = np.array(self.img.tolist())

        im = Image.fromarray(img, mode="RGBA")
        im = im.rotate(90, expand=True)
        im.save(self.output_file)


def main():
    input_files = []
    output_files = []
    start = 14.0
    increment = 0.4
    for i in range(36):
        input_files.append("parsed/output_" + "{:.1f}".format(start) + "s.txt")
        output_files.append(f"textures/{i}.png")
        start += increment

    for i in range(len(input_files)):
        Interpolator(input_files[i], output_files[i]).interpolate_points()


main()
