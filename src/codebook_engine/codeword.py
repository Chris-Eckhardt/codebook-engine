

class Codeword:

    _r = None
    _g = None
    _b = None
    _i = None
    _min_brightness = None
    _max_brightness = None
    _freq = None
    _lambda = None
    _first_access = None
    _last_access = None

    def __init__(self):
        pass

    def __repr__(self):
        return '[{},{},{}] - [{},{},{},{},{},{}]'.format(
            self.red(), self.green(), self.blue(), self.min_brightness(), self.max_brightness(),
            self.freq(), self.lam(), self.first_access(), self.last_access())

    def is_within(self, I):
        if self._max_brightness >= I >= self._min_brightness:
            return True
        else:
            return False

    ########################################
    #         GETTERS AND SETTERS          #
    ########################################

    def red(self, val=None):
        if val is None:
            return self._r
        else:
            self._r = int(val)

    def green(self, val=None):
        if val is None:
            return self._g
        else:
            self._g = int(val)

    def blue(self, val=None):
        if val is None:
            return self._b
        else:
            self._b = int(val)

    def min_brightness(self, val=None):
        if val is None:
            return self._min_brightness
        else:
            self._min_brightness = int(val)

    def max_brightness(self, val=None):
        if val is None:
            return self._max_brightness
        else:
            self._max_brightness = int(val)

    def freq(self, val=None):
        if val is None:
            return self._freq
        else:
            self._freq = val

    def lam(self, val=None):
        if val is None:
            return self._lambda
        else:
            self._lambda = val

    def first_access(self, val=None):
        if val is None:
            return self._first_access
        else:
            self._first_access = val

    def last_access(self, val=None):
        if val is None:
            return self._last_access
        else:
            self._last_access = val
