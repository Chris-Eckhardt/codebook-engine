import cv2


class FrameManager(object):

    num_of_frames = 0
    ret = False
    frame = None
    width = 0
    height = 0

    def __init__(self, path):
        print(' * using: "{}"'.format(path))
        self.path = path
        self.cap = cv2.VideoCapture(self.path)
        self.frame_width = 640  # int(self.cap.get(3)) # 340
        self.frame_height = 480  # int(self.cap.get(4)) # 260
        self.count_frames()

    def reset(self):
        self.cap = cv2.VideoCapture(self.path)

    def count_frames(self):
        while True:
            ret, f = self.cap.read()
            if ret is False:
                break
            self.num_of_frames += 1
        self.reset()
        print(' * {} frames captured'.format(self.num_of_frames))

    def get_next_frame(self):
        self.ret, f = self.cap.read()
        if self.ret is True:
            self.frame = cv2.resize(f, (self.frame_width, self.frame_height))
            return True
        return False

    def show_frame(self, wait=10):
        cv2.imshow('Capture Display', self.frame)
        if cv2.waitKey(wait) == ord('q'):
            self.close_window()

    def close_window(self):
        self.cap.release()
        cv2.destroyAllWindows()

    def __del__(self):
        self.cap.release()
        cv2.destroyAllWindows()
