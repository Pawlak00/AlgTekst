from dynamic_huffman import *
from static_huffman import *
from bitarray import bitarray
from os.path import getsize 
from time import perf_counter
from tabulate import tabulate
import numpy as np
class huff_compression():
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
raw_text_files= [['1kB','10kB','100kB','1MB'],['gutenberg1kB','gutenberg10kB','gutenberg100kB','gutenberg1MB'],
                    ['github1kB','github10kB','github100kB','github1MB']]
static_compressed='static.huf'
adaptive_compressed='adaptive.huf'
times_encode_adaptive=[[],[],[]]
times_decode_adaptive=[[],[],[]]
times_encode_static=[[],[],[]]
times_decode_static=[[],[],[]]
compress_coef_adapt=[[],[],[]]
compress_coef_stat=[[],[],[]]
for i in range(len(raw_text_files)):
    for raw_text_file in raw_text_files[i]:
        comp=huff_compression()
        comp.read_from_raw_file(raw_text_file)
        # measure static encode time
        static_comp_start=perf_counter()
        comp.compress('static')
        static_comp_end=perf_counter()
        # save static encode to file
        comp.save_compressed_to_file(static_compressed)
        # measure static decode
        static_read_start=perf_counter()
        comp.read_compressed_file(static_compressed)
        static_read_end=perf_counter()
        comp.code=None
        # measure dynamic encode
        dyn_comp_start=perf_counter()
        comp.compress('dynamic')
        dyn_comp_end=perf_counter()
        # save dynamic encode to file
        comp.save_compressed_to_file(adaptive_compressed)
        # measure dynamic decode
        dyn_read_start=perf_counter()
        comp.read_compressed_file(adaptive_compressed)
        dyn_read_end=perf_counter()
        print('OK' if comp.read_compressed_file(adaptive_compressed)==True else 'ERROR')
        times_encode_static[i].append(round(static_comp_end-static_comp_start,3))
        times_encode_adaptive[i].append(round(dyn_comp_end-dyn_comp_start,3))
        times_decode_static[i].append(round(static_read_end-static_read_start,3))
        times_decode_adaptive[i].append(round(dyn_read_end-dyn_read_start,3))
        compress_coef_stat[i].append(round((1-getsize(static_compressed)/getsize(raw_text_file))*100,2))
        compress_coef_adapt[i].append(round((1-getsize(adaptive_compressed)/getsize(raw_text_file))*100,2))
compress_coef_stat=np.array(compress_coef_stat).T.tolist()
compress_coef_adapt=np.array(compress_coef_adapt).T.tolist()
times_decode_static=np.array(times_decode_static).T.tolist()
times_decode_adaptive=np.array(times_decode_adaptive).T.tolist()
times_encode_static=np.array(times_encode_static).T.tolist()
times_encode_adaptive=np.array(times_encode_adaptive).T.tolist()
compress_coef_stat.insert(0,['random','gutenberg','github'])
compress_coef_adapt.insert(0,['random','gutenberg','github'])
times_decode_static.insert(0,['random','gutenberg','github'])
times_decode_adaptive.insert(0,['random','gutenberg','github'])
times_encode_static.insert(0,['random','gutenberg','github'])
times_encode_adaptive.insert(0,['random','gutenberg','github'])
print('wspolczynniki kompresji algorytmu statycznego')
print(tabulate(compress_coef_stat,headers='firstrow',showindex=['1kB','10kB','100kB','1MB']))
print('wspolczynniki kompresji algorytmu adaptacyjnego')
print(tabulate(compress_coef_adapt,headers='firstrow',showindex=['1kB','10kB','100kB','1MB']))
print('czas odkodowaniu kodu z algorytmu statycznego')
print(tabulate(times_decode_static,headers='firstrow',showindex=['1kB','10kB','100kB','1MB']))
print('czas odkodowaniu kodu z algorytmu adaptacyjnego')
print(tabulate(times_decode_adaptive,headers='firstrow',showindex=['1kB','10kB','100kB','1MB']))
print('czas zakodowania algorytmu statycznego')
print(tabulate(times_encode_static,headers='firstrow',showindex=['1kB','10kB','100kB','1MB']))
print('czas zakodowania kodu z algorytmu adaptacyjnego')
print(tabulate(times_encode_adaptive,headers='firstrow',showindex=['1kB','10kB','100kB','1MB']))