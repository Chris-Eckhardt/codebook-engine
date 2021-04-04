from codebook_engine.codebook_engine import CodebookEngine

if __name__ == '__main__':
    path = 'AN2957 (+ 30 min).MOV'
    cbe = CodebookEngine(path)
    cbe.init_codebooks()
    cbe.build_codebooks()
    cbe.temporal_filtering()
    cbe.build_output_file()
