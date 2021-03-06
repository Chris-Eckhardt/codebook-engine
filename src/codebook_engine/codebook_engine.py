import cv2
import json
import datetime
from codebook_engine.frame_manager import FrameManager
from codebook_engine.codebook import Codebook
from codebook_engine.model import Model
from codebook_engine.codeword import Codeword

###############################################################
#  CodebookEngine:
#
###############################################################

class CodebookEngine:

    black = [0, 0, 0]
    white = [255, 255, 255]

    data = []

    cw_created = 0

    def __init__(self):
        pass

    ###############################################################
    #  init_frame_manager:
    #
    #  params: source (name of file to be used),
    #   alpha, beta
    #  return: none
    ###############################################################

    def init_frame_manager(self, source, alpha=0.7, beta=1.1):
        if source != '':
            self.fm = FrameManager(source)
        self.mnrl_threshold = self.fm.num_of_frames / 2
        self.alpha = alpha # between 0.4 and 0.7
        self.beta = beta # between 1.1 and 1.5

    ###############################################################
    #  init_codebooks:
    #
    # params: none
    # return: none
    ###############################################################

    def init_codebooks(self):
        for y in range(0, self.fm.frame_height):
            temp = []
            for x in range(0, self.fm.frame_width):
                temp.append(Codebook(self.alpha, self.beta))
            self.data.append(temp)
        self.fm.reset()
        print(' * codebooks initialized with size {}, {}'.format(len(self.data[0]), len(self.data)))

    ###############################################################
    #  build_codebooks:
    #
    #  params: none
    #  return: none
    ###############################################################

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

    ###############################################################
    #  clean_lambdas:
    #
    #  params: none
    #  return: none
    ###############################################################

    def clean_lambdas(self):
        for y in range(0, self.fm.frame_height-1):
            for x in range(0, self.fm.frame_width-1):
                cb = self.data[y][x]
                for cw in cb.codewords:
                    cw.lam( max( cw.lam(), (self.fm.num_of_frames-cw.first_access()+cw.last_access()-1) ) )
        print(' * cleaned lambdas')

    ###############################################################
    #  temporal_filtering:
    #
    #  params: none
    #  return: none
    ###############################################################

    def temporal_filtering(self):
        for y in range(0, self.fm.frame_height-1):
            for x in range(0, self.fm.frame_width-1):
                cw_list = self.data[y][x].codewords
                for cw in cw_list:
                    if cw.lam() <= self.mnrl_threshold:
                        cw_list.remove(cw)
        print(' * temporal filtering complete')

    ###############################################################
    #  count_non_singltons:
    #
    # use: this function is only used for debug, 
    #   it has no other perpose
    ###############################################################

    def count_non_singltons(self):
        i = 0
        for y in range(0, self.fm.frame_height-1):
            for x in range(0, self.fm.frame_width-1):
                cw_list = self.data[y][x].codewords
                if len(cw_list) > 1:
                    i += 1
        print('i:{}'.format(i))

    ###############################################################
    #  save_model:
    #
    #  params: name (name of model to be written)
    #  return: none
    ###############################################################

    def save_model(self, name):
        data = self.convert_data()
        model = Model(name=name,alpha=self.alpha, beta=self.beta, height=self.fm.frame_height, width=self.fm.frame_width, data=data)
        j_model = json.dumps(model.__dict__)
        with open( '{}.json'.format(name), 'w') as fd:
            fd.write(j_model)
        print(' * model [{}.json] was successfully created.'.format(name))

    ###############################################################
    #  convert_data:
    #
    #  params: none
    #  return: matrix of codebooks represented as list of strings
    ###############################################################

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

    ###############################################################
    #  load_model:
    #
    #  params: source (name of model file)
    #  return: none
    ###############################################################

    def load_model(self, source):
        with open(source, 'r') as json_file:
            i = json.load(json_file)
            self.alpha = i['alpha']
            self.beta = i['beta']
            self.data = []
            for y in range(0, int(i['height'])-1):
                temp = []
                for x in range(0, int(i['width'])-1):
                    cb = Codebook(alpha=self.alpha, beta=self.beta)
                    temp.append(cb)
                self.data.append(temp)
            for y in range(0, int(i['height'])-1):
                for x in range(0, int(i['width'])-1):
                    cb = self.data[y][x]
                    for v in i['data'][y][x]:
                        cb.codewords.append(Codeword(v))
        print(' * model loaded : {}'.format(source))

    ###############################################################
    #  build_output_file:
    #
    #  params: source (not used, needs to be removed),
    #   out (name of output file to be written to memory)
    #  return: none
    ###############################################################
                        
    def build_output_file(self, source='', out=''):
        t = 1
        self.fm.output_init(out)
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
