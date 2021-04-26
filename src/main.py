from codebook_engine.codebook_engine import CodebookEngine
from codebook_engine.codeword import Codeword
import time
import sys
from codebook_engine.cb_shell import CbShell


if __name__ == '__main__':
    shell = CbShell()
    shell.run()
    # a = 0.4
    # b = 1.5
    # if len(sys.argv) > 2:
    #     a = float(sys.argv[1])
    #     b = float(sys.argv[2])

    # start = time.time()
    
    # path1 = 'AN2957 (+ 30 min).MOV'
    # path2 = 'D-PZQ(test1) 10a_t001.MOV'
    # cbe = CodebookEngine(path2, alpha=a, beta=b)
    # cbe.init_codebooks()
    # cbe.build_codebooks()
    # cbe.clean_lambdas()
    # cbe.temporal_filtering()

    # stop = time.time()
    # elapsed = (stop - start)
    # print("--- %s seconds ---" % elapsed)
    # print('--- {} minutes ---'.format(elapsed/60))

    # #cbe.save_model()

    # cbe.build_output_file(path1)
