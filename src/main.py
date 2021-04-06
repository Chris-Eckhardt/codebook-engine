from codebook_engine.codebook_engine import CodebookEngine
import time


if __name__ == '__main__':
    start = time.time()
    
    path = 'AN2957 (+ 30 min).MOV'
    cbe = CodebookEngine(path)
    cbe.init_codebooks()
    cbe.build_codebooks()
    cbe.temporal_filtering()

    stop = time.time()
    elapsed = (stop - start)
    print("--- %s seconds ---" % elapsed)
    print('--- {} minutes ---'.format(elapsed/60))

    cbe.build_output_file()
