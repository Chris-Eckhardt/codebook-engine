from codebook_engine.model import Model
from codebook_engine.codebook_engine import CodebookEngine
import json

if __name__ == '__main__':
    cbe = CodebookEngine('', 0, 0)
    cbe.load_model('test_name_1.json')
    print(cbe.data[0][0])