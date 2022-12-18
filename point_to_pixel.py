import math
import numpy as np

PIXEL_SIZE = 0.62
X_DIFF = 113.988857
Y_DIFF = 127.588813

# column_0 = [1.30739393463136, 0, 0, 1.0848834056023555, ... , 1.3015098142343031, 0,0,0,0,0,,0,0,0,0,0]

class Interpolator():
    def __init__(self):
        self.input_file = open("flow_output_vm.txt", "r")
        self.x_size = math.ceil(X_DIFF / PIXEL_SIZE) + 1
        self.y_size = math.ceil(Y_DIFF / PIXEL_SIZE) + 1
        self.img = np.zeros([self.x_size, self.y_size])

        self.interpolate_list = []
        self.y_prev = 0
        self.y_i = 0
        self.x_i = 0
        self.i = 0

    def read_first_line(self):
        for line in self.input_file:
            line = line.split(' ')
            self.y_prev = float(line[1])
            v_m = float(line[2])
            self.img[self.x_i, self.y_i] = v_m
            self.i+=1
            break

    def run(self):
        self.read_first_line()

        for line in self.input_file:
            line = line.split(' ')
            x = float(line[0])
            y = float(line[1])
            v_m = float(line[2])

            while self.y_prev > y:
                self.y_prev -= PIXEL_SIZE
                self.y_i += 1
                self.interpolate_list.append((self.x_i, self.y_i))
            
            self.img[self.x_i, self.y_i] = v_m
            if len(self.interpolate_list) > 1: self.interpolate()

            if self.i == 116:
               self.read_next_column()
            else:
                y -= y - self.y_prev
                self.y_prev = y
                
                self.i+=1

        self.save()

    def interpolate(self):
        self.interpolate_list.remove(self.interpolate_list[-1])
        v1 = (self.x_i, self.interpolate_list[0][1] - 1)
        v2 = (self.x_i, self.interpolate_list[-1][1] + 1)
        discount = abs(self.img[v1] - self.img[v2]) / (len(self.interpolate_list) + 1)

        for i in range(len(self.interpolate_list)):
            self.img[self.interpolate_list[i]] = self.img[v1] - discount * (i + 1)

        self.interpolate_list.clear()

    def read_next_column(self):
        for line in self.input_file:
            line = line.split(' ')
            y = float(line[1])
            v_m = float(line[2])

            self.i = 0 
            self.y_i = 0
            self.x_i += 1
            self.img[self.x_i, self.y_i] = v_m
            self.y_prev = y
            self.i+=1
            break

    def save(self):
        out = open("output.csv", "w")
        for x in range(111):
            for y in range(self.y_size):
                out.write(f"{x},{y},{self.img[x, y]}\n")

def main():
    Interpolator().run()

main()
