from codebook_engine.model import Model
from codebook_engine.codebook_engine import CodebookEngine
import json


class Thing:

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name


class Test:

    li = [Thing('this'), Thing('that'), Thing('these')]

    def __init__(self):
        pass

    def __repr__(self):
        pass

    def get_cw_as_list(self):
        li = [x.__repr__() for x in self.li]
        return li

if __name__ == '__main__':
    test = Test()
    print(test.get_cw_as_list())
    #cbe = CodebookEngine('', 0, 0)
    #cbe.load_model('test_name_1.json')
    