import cv2
import json
import datetime
from codebook_engine.frame_manager import FrameManager
from codebook_engine.codebook import Codebook
from codebook_engine.model import Model
from codebook_engine.codeword import Codeword


class CodebookEngine:

    path_to_assets = 'assets/'
    path_to_output = 'output/'
    path_to_models = 'models/'

    black = [0, 0, 0]
    white = [255, 255, 255]

    data = []

    cw_created = 0

    def __init__(self, source='', alpha=0.7, beta=1.1):
        if source != '':
            self.fm = FrameManager(self.path_to_assets + source)
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

    def count_non_singltons(self):
        i = 0
        for y in range(0, self.fm.frame_height-1):
            for x in range(0, self.fm.frame_width-1):
                cw_list = self.data[y][x].codewords
                if len(cw_list) > 1:
                    i += 1
        print('i:{}'.format(i))

    def save_model(self, name):
        data = self.convert_data()
        model = Model(name=name, height=self.fm.frame_width, width=self.fm.frame_width, data=data)
        j_model = json.dumps(model.__dict__)
        with open( '{}{}.json'.format(self.path_to_models, name), 'w') as fd:
            fd.write(j_model)
        print(' * model [{}.json] was successfully created.'.format(name))

    def convert_data(self):
        a = []
        for y in range(0, self.fm.frame_height-1):
            b = []
            for x in range(0, self.fm.frame_width-1):
                c = []
                cw_list = self.data[y][x].codewords
                for cw in cw_list:
                    c.append(cw.__repr__())
                b.append(c)
            a.append(b)
        return a

    def load_model(self, source):
        with open(self.path_to_models + source, 'r') as json_file:
            i = json.load(json_file)
            self.data = []
            for y in range(0, int(i['height'])-1):
                temp = []
                for x in range(0, int(i['width'])-1):
                    cb = Codebook()
                    temp.append(cb)
                self.data.append(temp)
            for y in range(0, int(i['height'])-1):
                for x in range(0, int(i['width'])-1):
                    for v in i['data'][y]:
                        print(i['data'])
            

    def build_output_file(self, path='', name=''):
        self.fm = FrameManager(self.path_to_assets + path)
        t = 1
        self.fm.output_init(self.path_to_output + name)
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
