from .codeword import Codeword
import math

###############################################################
#  Codebook object class
###############################################################

class Codebook(object):

    def __init__(self, alpha, beta):
        self.codewords = []
        self.alpha = alpha
        self.beta = beta

    ###############################################################
    #  process_pixel:
    #
    #  params: pixel (rgb values as list), t (current frame number)
    #  returns: if pixel matches codeword: adds pixel to codeword, 
    #   else create a new codeword and append it to the self.codewords
    ###############################################################

    def process_pixel(self, pixel, t):
        for cw in self.codewords:
            if self.is_match(cw, pixel):
                self.add_pixel_to_cw(cw, pixel, t)
                return
        self.codewords.append(self.new_codeword(pixel, t))

    ###############################################################
    #  is_match:
    #
    #  params: cw (codeword), 
    #   pixel (new pixel rgb values being checked)
    #  returns: true if pixel matches the codeword, else false
    ###############################################################

    def is_match(self, cw, pixel):
        r = pow(int(pixel[0]), 2)
        g = pow(int(pixel[1]), 2)
        b = pow(int(pixel[2]), 2)
        brightness = math.sqrt(r + g + b)
        mini = int(cw.min_brightness() * self.alpha)
        maxi = int(cw.max_brightness() * self.beta)
        if mini <= brightness <= maxi:
            return True
        else:
            return False

    ###############################################################
    #  add_pixel_to_cw:
    #
    #  params: cw (codeword), 
    #   pixel (new pixel rgb values to be added to this codeword),
    #   t (current frame number)
    #  returns: none
    ###############################################################

    def add_pixel_to_cw(self, cw, pixel, t):
        r = int(pixel[0])
        g = int(pixel[1])
        b = int(pixel[2])
        brightness = math.sqrt(pow(r, 2) + pow(g, 2) + pow(b, 2))
        cw.red(self.calc_new_color(curr=cw.red(), new=r, freq=cw.freq()))
        cw.green(self.calc_new_color(curr=cw.green(), new=g, freq=cw.freq()))
        cw.blue(self.calc_new_color(curr=cw.blue(), new=b, freq=cw.freq()))
        cw.min_brightness(min(brightness, cw.min_brightness()))
        cw.max_brightness(max(brightness, cw.max_brightness()))
        cw.freq(cw.freq() + 1)
        cw.lam(max(cw.lam(), t - cw.last_access()))
        cw.last_access(t)

    ###############################################################
    #  calc_new_color:
    #
    #  params: curr (current color value, 0-255), 
    #   new (new color value being added, 0-255),
    #   freq (the frequency of the relevent codeword)
    #  returns: the new adjusted color value (0-255)
    ###############################################################

    def calc_new_color(self, curr, new, freq):
        num = (freq * curr) + new
        den = freq + 1
        return num / den

    ###############################################################
    #  new_codeword:
    #
    #  params: pixel (rgb values as list), t (current frame number)
    #  returns: a list of the string representations 
    #   of all codewords contained in self.data
    ###############################################################

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

    ###############################################################
    #  bdg:
    #
    #  params: pixel (rgb values as list)
    #  returns: true if pixel matches an existing codeword, 
    #   else false
    ###############################################################

    def bgd(self, pixel):
        for cw in self.codewords:
            if self.is_match(cw, pixel):
                return True
        return False

    ###############################################################
    #  get_cw_as_list:
    #
    #  params: none
    #  returns: a list of the string representations 
    #   of all codewords contained in self.data
    ###############################################################

    def get_cw_as_list(self):
        li = [x.__repr__() for x in self.codewords]
        return li
