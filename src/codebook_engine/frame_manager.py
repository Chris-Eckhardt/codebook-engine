import cv2

###############################################################
#  Frame Manager:
#
###############################################################

class FrameManager(object):

    num_of_frames = 0
    ret = False
    frame = None
    width = 0
    height = 0
    out = None

    def __init__(self, path):
        print(' * using: "{}"'.format(path))
        self.path = path
        self.cap = cv2.VideoCapture(self.path)
        self.frame_width = 640  # int(self.cap.get(3)) # 340
        self.frame_height = 480  # int(self.cap.get(4)) # 260
        self.count_frames()

    ###############################################################
    #  reset:
    #
    #  use: reset video capture
    ###############################################################

    def reset(self):
        self.cap = cv2.VideoCapture(self.path)

    ###############################################################
    #  count_frames:
    #
    #  use: determine the number of frames in video file
    ###############################################################

    def count_frames(self):
        while True:
            ret, f = self.cap.read()
            if ret is False:
                break
            self.num_of_frames += 1
        self.reset()
        print(' * {} frames captured'.format(self.num_of_frames))

    ###############################################################
    #  get_next frame:
    #
    #  use: iterates to next frame (if frame exists)
    #  returns true if next frame exists, false if it does not
    #  NOTE: all frames are resized to 640 x 480 here to 
    #   reduce training time
    ###############################################################

    def get_next_frame(self):
        self.ret, f = self.cap.read()
        if self.ret is True:
            self.frame = cv2.resize(f, (self.frame_width, self.frame_height))
            return True
        return False

    ###############################################################
    #  show_frame:
    #
    #  create a window and display the current frame
    ###############################################################

    def show_frame(self, wait=10):
        cv2.imshow('Capture Display', self.frame)
        if cv2.waitKey(wait) == ord('q'):
            self.close_window()

    ###############################################################
    #  close window:
    #
    #  use: close cv2 window and release resources
    ###############################################################

    def close_window(self):
        self.cap.release()
        cv2.destroyAllWindows()

    ###############################################################
    #  output_init:
    #
    #  params: filename (name of file to be created)
    #  use: initialize resources required for creating avi file
    ###############################################################

    def output_init(self, filename):
        self.out = cv2.VideoWriter(
            filename+'.avi',
            cv2.VideoWriter_fourcc(*'DIVX'),
            20.0,
            (self.frame_width, self.frame_height)
        )

    ###############################################################
    #  output_write_frame:
    #
    #  use: write current frame to output file
    ###############################################################

    def output_write_frame(self):
        self.out.write(self.frame)

    ###############################################################
    #  output_release:
    #
    #  use: release cv2 video writer resources
    ###############################################################

    def output_release(self):
        self.out.release()

    ###############################################################
    #  destructor:
    #
    #  use: release all cv2 related resources
    ###############################################################

    def __del__(self):
        if self.out is not None:
            self.out.release()
        self.cap.release()
        cv2.destroyAllWindows()
