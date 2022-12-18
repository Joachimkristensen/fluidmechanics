import math
import collections

FOLDER = "sims/"


def main():
    input_files = []
    output_files = []
    start = 14.0
    increment = 0.4

    for i in range(36):
        input_files.append(FOLDER + "{:.1f}".format(start) + "s.txt")
        output_files.append("parsed/output_" +
                            "{:.1f}".format(start) + "s.txt")
        start += increment

    for i in range(len(input_files)):
        with open(input_files[i]) as input_file:
            for _ in range(9):
                next(input_file)

            z_flags = {}
            surfaces = {}
            v_m = []
            x_max = 0
            x_min = 0
            y_max = 0
            y_min = 0

            # x  y  z  vf  u  v  w
            first_z = 0
            is_first_z = True

            for line in input_file:
                line = line.strip().strip().split()
                line = [float(x) for x in line]
                x_max = x_min = line[0]
                y_max = y_min = line[1]
                first_z = line[2]
                break

            input_file = open(input_files[i], "r")

            for _ in range(9):
                next(input_file)
            for line in input_file:
                line_org = line.strip().strip().split()
                line = [float(x) for x in line_org]

                x = line[0]
                y = line[1]
                z = line[2]
                vf = line[3]

                if z != first_z:
                    is_first_z = False

                if is_first_z:
                    if (0.0 < vf < 1.0):
                        u = line[4]
                        v = line[5]
                        w = line[6]
                        n = u*u + v*v + w*w
                        v_m = n / math.sqrt(n) if n != 0 else 0

                        surfaces[(x, y)] = v_m

                else:
                    if (0.0 < vf < 1.0) or (vf == 0.0 and z_flags[(x, y)][1] == 1.0):
                        u = line[4]
                        v = line[5]
                        w = line[6]
                        n = u*u + v*v + w*w
                        v_m = n / math.sqrt(n) if n != 0 else 0

                        surfaces[(x, y)] = v_m

                x_max = x if x > x_max else x_max
                x_min = x if x < x_min else x_min
                y_max = y if y > y_max else y_max
                y_min = y if y < y_min else y_min
                z_flags[(x, y)] = (z, vf)

            surfaces = collections.OrderedDict(
                sorted(surfaces.items(), key=lambda key: key[0], reverse=False))

            out_file = open(output_files[i], "w")
            for key, v_m in surfaces.items():
                out_file.write(f"{key[0]} {key[1]} {v_m}\n")


main()
