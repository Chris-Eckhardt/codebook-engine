from .codeword import Codeword
import math

class Codebook(object):

    alpha = 0.6  # between 0.4 and 0.7
    beta = 1.1  # between 1.1 and 1.5

    def __init__(self):
        self.codewords = []

    def process_pixel(self, pixel, t):
        for cw in self.codewords:
            if self.is_match(cw, pixel):
                self.add_pixel_to_cw(cw, pixel, t)
                return
        self.codewords.append(self.new_codeword(pixel, t))

    def is_match(self, cw, pixel):
        r = pow(int(pixel[0]), 2)
        g = pow(int(pixel[1]), 2)
        b = pow(int(pixel[2]), 2)
        brightness = math.sqrt(r + g + b)
        min = int(cw.min_brightness() * self.alpha)
        max = int(cw.max_brightness() * self.beta)
        if min <= brightness <= max:
            return True
        else:
            return False

    def add_pixel_to_cw(self, cw, pixel, t):
        r = int(pixel[0])
        g = int(pixel[1])
        b = int(pixel[2])
        brightness = math.sqrt(pow(r, 2) + pow(g, 2) + pow(b, 2))
        cw.red(self.calc_new_color(cw.red(), r, cw.freq()))
        cw.green(self.calc_new_color(cw.green(), g, cw.freq()))
        cw.blue(self.calc_new_color(cw.blue(), b, cw.freq()))
        cw.min_brightness(min(brightness, cw.min_brightness()))
        cw.max_brightness(max(brightness, cw.max_brightness()))
        cw.freq(cw.freq() + 1)
        cw.lam(max(cw.lam(), t - cw.last_access()))
        cw.last_access(t)

    def calc_new_color(self, curr, new, freq):
        num = (freq * curr) + new
        den = freq + 1
        return num / den

    def new_codeword(self, pixel, t):
        r = int(pixel[0])
        g = int(pixel[1])
        b = int(pixel[2])
        brightness = math.sqrt(pow(r, 2) + pow(g, 2) + pow(b, 2))
        cw = Codeword()
        cw.red(r)
        cw.green(g)
        cw.blue(b)
        cw.max_brightness(brightness)
        cw.min_brightness(brightness)
        cw.freq(1)
        cw.lam(t-1)
        cw.first_access(t)
        cw.last_access(t)
        return cw

    def bgd(self, pixel):
        for cw in self.codewords:
            if self.is_match(cw, pixel):
                return True
        return False
