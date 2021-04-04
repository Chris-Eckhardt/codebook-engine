import cv2
import os
from codebook_engine.frame_manager import FrameManager
from codebook_engine.codebook import Codebook


class CodebookEngine:

    path_to_assets = 'assets/'
    path_to_output = 'output/'

    black = [0, 0, 0]
    white = [255, 255, 255]

    data = []

    cw_created = 0

    def __init__(self, path):
        print(os.getcwd())
        self.fm = FrameManager(self.path_to_assets + path)
        self.mnrl_threshold = self.fm.num_of_frames / 2

    def init_codebooks(self):
        for y in range(0, self.fm.frame_height):
            temp = []
            for x in range(0, self.fm.frame_width):
                temp.append(Codebook())
            self.data.append(temp)
        self.fm.reset()
        print(' * codebooks initialized with size {}, {}'.format(len(self.data[0]), len(self.data)))

    def build_codebooks(self):
        t = 1
        while self.fm.get_next_frame():
            print(t)
            for y in range(0, self.fm.frame_height-1):
                for x in range(0, self.fm.frame_width-1):
                    pixel = self.fm.frame[y][x]
                    cb = self.data[y][x]
                    cb.process_pixel(pixel, t)
            t += 1
        self.fm.reset()
        print(' * built codebooks')

    def temporal_filtering(self):
        for y in range(0, self.fm.frame_height-1):
            for x in range(0, self.fm.frame_width-1):
                cw_list = self.data[y][x].codewords
                for cw in cw_list:
                    if cw.lam() <= self.mnrl_threshold:
                        cw_list.remove(cw)
        print(' * temporal filtering complete')

    def build_output_file(self):
        # input(' * press any key to continue ...')
        t = 1
        out = cv2.VideoWriter(
            self.path_to_output+'output.avi',
            cv2.VideoWriter_fourcc(*'DIVX'),
            20.0,
            (self.fm.frame_width, self.fm.frame_height)
        )
        while self.fm.get_next_frame():
            print(t)
            for y in range(0, self.fm.frame_height-1):
                for x in range(0, self.fm.frame_width-1):
                    pixel = self.fm.frame[y][x]
                    cw = self.data[y][x]
                    if cw.bgd(pixel):
                        self.fm.frame[y][x] = self.black
                    else:
                        self.fm.frame[y][x] = self.white
            out.write(self.fm.frame)
            t += 1
        out.release()
        self.fm.cap.release()
        print(' * output file built')




