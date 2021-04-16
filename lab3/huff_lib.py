from dynamic_huffman import *
from static_huffman import *
from bitarray import bitarray
from os.path import getsize 
from time import perf_counter
class huff_compression():
    """docstring for huff_compressed"""
    def __init__(self, text=None):
        self.text=text
        self.code=None
        self.text_compressed=None
        self.adaptive=None
        self.static=None
    def compress(self,huff_method):
        """compress text using dynamic or static huffman algorithm"""
        if huff_method=='dynamic':
            self.adaptive=adaptive_huffman()
            self.code=self.adaptive.generate_code(self.text)
        elif huff_method=='static':
            self.static=static_huffman()
            self.code=self.static.generate_code(self.text) 
    def save_compressed_to_file(self,file_name):
        # print(self.code)
        res=bitarray()
        for v in self.text:
            res.extend(self.code[v])
        with open(file_name,"wb") as file:
            file.write(len(self.code).to_bytes(8,'big'))#number of signs
            for v in self.code:
                file.write(len(bytes(v,'utf-8')).to_bytes(8,'big'))
                file.write(bytes(v,'utf-8'))
            for v in self.code:
                file.write(len(self.code[v]).to_bytes(8,'big'))
                self.code[v].tofile(file)
            file.write(len(res).to_bytes(8,'big'))
            res.tofile(file)#code
    def read_compressed_file(self,file_name):
        with open(file_name,"rb") as file:
            n_of_signs=int.from_bytes(file.read(8),'big')
            signs=[]
            codes=[]
            # print(n_of_signs)
            for i in range(0,n_of_signs,1):
                size=int.from_bytes(file.read(8),'big')
                signs.append(file.read(size).decode('utf-8'))
                # print(signs[-1])
            for i in range(0,n_of_signs,1):
                size=int.from_bytes(file.read(8),'big')
                tmp=file.read(size//8 if size%8==0 else size//8+1)
                a=bitarray()
                a.frombytes(tmp)
                codes.append(a[:size])
            decode={code.to01():sign for code,sign in list(zip(codes,signs))}
            code_size=int.from_bytes(file.read(8),'big')
            b=bitarray()
            b.fromfile(file)
            k=0;
            decoded_text=''
            for i in range(code_size+1):
                pref=b[k:i].to01()
                if pref in decode:
                    decoded_text+=decode[pref]
                    k=i
            return decoded_text==self.text
    def read_from_raw_file(self,file_name):
        with open(file_name,"r") as file:
            lines=file.readlines()
            res=''
            for l in lines:
                res+=l
            self.text=res
# '1kB','10kB','100kB','1MB','gutenberg'
raw_text_files= ['1kB','10kB','100kB','1MB','gutenberg1kB','gutenberg10kB','gutenberg100kB','gutenberg1MB',
                    'github1kB','github10kB','github100kB','github1MB']
static_compressed='static.huf'
adaptive_compressed='adaptive.huf'
# raw_text_file='gutenberg'
# comp=huff_compression()
# comp.read_from_raw_file(raw_text_file)
# comp.compress('static')
# comp.save_compressed_to_file(adaptive_compressed)
# print(comp.read_compressed_file(adaptive_compressed))
for raw_text_file in raw_text_files:
    comp=huff_compression()
    comp.read_from_raw_file(raw_text_file)
    s_t0=perf_counter()
    comp.compress('static')
    s_t1=perf_counter()
    comp.save_compressed_to_file(static_compressed)
    a_t0=perf_counter()
    comp.compress('dynamic')
    a_t1=perf_counter()
    comp.save_compressed_to_file(adaptive_compressed)
    print('OK' if comp.read_compressed_file(adaptive_compressed)==True else 'ERROR',
        raw_text_file,
        'static encode time ',round(s_t1-s_t0,3),
        'adaptive endoce time',round(a_t1-a_t0,3))
    se_t0=perf_counter()
    comp.read_compressed_file(static_compressed)
    se_t1=perf_counter()
    ae_t0=perf_counter()
    comp.read_compressed_file(adaptive_compressed)
    ae_t1=perf_counter()
    print('static decode: ',round(se_t1-se_t0,3),'adaptive decode: ',round(ae_t1-ae_t0,3))
    print('text file size',raw_text_file,' ',
        getsize(raw_text_file),' static ',
        getsize(static_compressed),' adaptive ',
        getsize(adaptive_compressed),' adaptive ratio ',
        round((1-getsize(adaptive_compressed)/getsize(raw_text_file))*100,2),
        ' static ratio ',round((1-getsize(static_compressed)/getsize(raw_text_file))*100,2))
    print('\n')