import cv2
import datetime
from codebook_engine.frame_manager import FrameManager
from codebook_engine.codebook import Codebook


class CodebookEngine:

    path_to_assets = 'assets/'
    path_to_output = 'output/'
    path_to_models = 'models/'

    black = [0, 0, 0]
    white = [255, 255, 255]

    data = []

    cw_created = 0

    def __init__(self, path, alpha, beta):
        self.fm = FrameManager(self.path_to_assets + path)
        self.mnrl_threshold = self.fm.num_of_frames / 2
        self.alpha = alpha # between 0.4 and 0.7
        self.beta = beta # between 1.1 and 1.5

    def init_codebooks(self):
        for y in range(0, self.fm.frame_height):
            temp = []
            for x in range(0, self.fm.frame_width):
                temp.append(Codebook(self.alpha, self.beta))
            self.data.append(temp)
        self.fm.reset()
        print(' * codebooks initialized with size {}, {}'.format(len(self.data[0]), len(self.data)))

    def build_codebooks(self):
        t = 1
        while self.fm.get_next_frame():
            for y in range(0, self.fm.frame_height-1):
                for x in range(0, self.fm.frame_width-1):
                    pixel = self.fm.frame[y][x]
                    cb = self.data[y][x]
                    cb.process_pixel(pixel, t)
            t += 1
        self.fm.reset()
        print(' * built codebooks')

    def clean_lambdas(self):
        for y in range(0, self.fm.frame_height-1):
            for x in range(0, self.fm.frame_width-1):
                cb = self.data[y][x]
                for cw in cb.codewords:
                    cw.lam( max( cw.lam(), (self.fm.num_of_frames-cw.first_access()+cw.last_access()-1) ) )
        print(' * cleaned lambdas')

    def temporal_filtering(self):
        for y in range(0, self.fm.frame_height-1):
            for x in range(0, self.fm.frame_width-1):
                cw_list = self.data[y][x].codewords
                for cw in cw_list:
                    if cw.lam() <= self.mnrl_threshold:
                        cw_list.remove(cw)
        print(' * temporal filtering complete')

    def save_model(self):
        with open( '{}{}_model.txt'.format(self.path_to_models, datetime.date.today()), 'w') as fd:
            fd.write(str(self.fm.frame_height) + '\n')
            fd.write(str(self.fm.frame_width) + '\n')
            for y in range(0, self.fm.frame_height-1):
                for x in range(0, self.fm.frame_width-1):
                    cw_list = self.data[y][x].codewords
                    fd.write(str(cw_list))
                fd.write('\n-----------\n')
            fd.write('\n-- eof')

    def load_model(self, path):
        pass

    def build_output_file(self, path=''):
        self.fm = FrameManager(self.path_to_assets + path)
        t = 1
        self.fm.output_init(self.path_to_output+'{}-a{}-b{}'.format(datetime.date.today(), self.alpha, self.beta))
        while self.fm.get_next_frame():
            for y in range(0, self.fm.frame_height-1):
                for x in range(0, self.fm.frame_width-1):
                    pixel = self.fm.frame[y][x]
                    cb = self.data[y][x]
                    if cb.bgd(pixel):
                        self.fm.frame[y][x] = self.black
                    else:
                        self.fm.frame[y][x] = self.white
            self.fm.output_write_frame()
            t += 1
        self.fm.output_release()
        self.fm.cap.release()
        print(' * output file built')
