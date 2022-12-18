MAX_V = 25
MIN_V = 3.1

SEGMENT_SIZE = 8
SEGMENT_STEP = MAX_V / SEGMENT_SIZE

BLUE = (0.0, (0, 0, 255))
TURQUOISE = (
    3.5, (64, 224, 208))
LIGHTGREEN = (7.0, (144, 238, 144))
GREEN = (10.5, (0, 128, 0))
YELLOW = (14.0, (255, 255, 0))
ORANGE = (17.5, (255, 165, 0))
SALMON = (21.0, (250, 128, 114))
RED = (25.0, (255, 0, 0))


class ColorThing:
    def __init__(self):
        pass

    def v_interval(self, v):
        if BLUE[0] < v < TURQUOISE[0]:
            return self.v_to_rgb(v, BLUE, TURQUOISE)
        elif TURQUOISE[0] < v < LIGHTGREEN[0]:
            return self.v_to_rgb(v, TURQUOISE, LIGHTGREEN)
        elif LIGHTGREEN[0] < v < GREEN[0]:
            return self.v_to_rgb(v, LIGHTGREEN, GREEN)
        elif GREEN[0] < v < YELLOW[0]:
            return self.v_to_rgb(v, GREEN, YELLOW)
        elif YELLOW[0] < v < ORANGE[0]:
            return self.v_to_rgb(v, YELLOW, ORANGE)
        elif ORANGE[0] < v < SALMON[0]:
            return self.v_to_rgb(v, ORANGE, SALMON)
        elif SALMON[0] < v < RED[0]:
            return self.v_to_rgb(v, SALMON, RED)
        else:
            return (255, 0, 0, 255)

    def v_to_rgb(self, v, c1, c2):
        c1_red = c1[1][0]
        c1_green = c1[1][1]
        c1_blue = c1[1][2]

        c2_red = c2[1][0]
        c2_green = c2[1][1]
        c2_blue = c2[1][2]

        start_diff = v - c1[0]
        diff = c2[0] - c1[0]
        percentile = start_diff / diff

        R = (c1_red * (1 - percentile) + c2_red * percentile)
        G = (c1_green * (1 - percentile) + c2_green * percentile)
        B = (c1_blue * (1 - percentile) + c2_blue * percentile)

        return (round(R), round(G), round(B), 0 if v < 3.0 else 255)
