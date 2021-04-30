import numpy as np
from spacy.language import Language
from spacy.tokenizer import Tokenizer
from spacy.vocab import Vocab
import spacy
def LCS(A,B,backtrace=False):
    m=len(A)
    n=len(B)
    F=[[]for i in range(m+1)]
    for i in range(m+1):
        F[i]=[0]*(n+1)
    # print(F)
    for i in range(1,m+1):
        for j in range(1,n+1):
            if A[i-1]==B[j-1]:
                F[i][j]=F[i-1][j-1]+1
            else:
                F[i][j]=max(F[i-1][j],F[i][j-1])
    i,j=m,n
    out=[]
    while i>0 and j>0:
        if A[i-1]==B[j-1]:
            out.append((A[i-1],i-1))
            i-=1
            j-=1
        elif F[i-1][j]>F[i][j-1]:
            i-=1
        else:
            j-=1
    out.reverse()
    return F[m][n],out if backtrace==True else F[m][n]
def remove_random(percentage,tokens):
    n_to_rm=int(percentage*len(tokens))
    res=[]
    for t in tokens:
        if np.random.uniform()>percentage:
            res.append(t)
    return res
def diff(file1,file2):
    f=open(file1,"r")
    f1=open(file2,"r")
    tokens1,tokens2=f.readlines(),f1.readlines()
    lcs_len,lcs=LCS(tokens1,tokens2,backtrace=True)
    print('length of lines lcs is : ',lcs_len)
    for i in range(1,lcs_len):
        if lcs[i][1]-lcs[i-1][1]>1:
            for j in range(lcs[i-1][1]+1,lcs[i][1]):
                if j<len(tokens1) and j<len(tokens2):
                    print(file1,' line ',j+1,' > ',tokens1[j])
                    print(file2,' line ',j+1, ' > ',tokens2[j])
def make_files(file_name):
    with open(file_name) as file:
        text=file.read()
        vocab = Language(Vocab()).vocab
        tokenizer = Tokenizer(vocab)
        tokens = tokenizer(text)
        text1 = remove_random(0.03,tokens)
        text2 = remove_random(0.03,tokens)
        with open('text1.txt', 'w') as new_file:
            for token in text1:
                new_file.write(token.text_with_ws)
        with open('text2.txt', 'w') as new_file:
            for token in text2:
                new_file.write(token.text_with_ws)
        print('lcs of tokens sequence is: ',LCS(text1,text2)[0])        
make_files('text.txt')
diff('text1.txt','text2.txt')