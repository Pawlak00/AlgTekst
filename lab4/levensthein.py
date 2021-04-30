import editdistance

def delta(a,b):
    return 0 if a==b else 1
def levenshtein_dist(t1,t2):
    m=len(t1)
    n=len(t2)
    d=[[0 for i in range(n+1)] for i in range(m+1)]
    for i in range(m+1):
        d[i][0]=i
    for i in range(n+1):
        d[0][i]=i
    for i in range(1,m+1,1):
        for j in range(1,n+1,1):
            cost=delta(t1[i-1],t2[j-1])
            d[i][j]=min(d[i-1][j]+1,d[i][j-1]+1,d[i-1][j-1]+cost)
    ans=d[m][n]
    print('t1',t1)
    print('t2',t2)
    print('+x+ - symbol x added \n/x/ - previous symbol changed to x\n- - symbol removed ')
    while m!=0 or n!=0:
        (last_m,last_n)=min([(m-1,n),(m,n-1),(m-1,n-1)],key=lambda x:(d[x[0]][x[1]],x))
        if (last_m,last_n)==(m-1,n-1):
            if d[last_m][last_n]<d[m][n]:
                t2=t2[:last_n]+t1[last_m]+t2[last_n+1:]
                print(t2[:last_n]+'/'+t1[last_m]+'/'+t2[last_n+1:])
            (m,n)=(m-1,n-1)
        if (last_m,last_n)==(m-1,n):
            t2=t2[:last_n]+t1[last_m]+t2[last_n:]
            print(t2[:last_n]+'+'+t1[last_m]+'+'+t2[last_n:])
            m-=1
        if (last_m,last_n)==(m,n-1):
            print(t2[:last_n]+'-'+t2[last_n+1:])
            t2=t2[:last_n]+t2[last_n+1:]
            n-=1
    print('OK' if t1==t2 else 'ERROR')
    return ans
def levenhtein_test():
    test=[('los','kloc'),('Łódź','Lodz'),('kwintesencja','quintessence'),('ATGAATCTTACCGCCTCG','ATGAGGCTCTGGCCCCTG')]
    for a,b in test:
        print('#######################################')
        print('OK' if levenshtein_dist( a, b)==editdistance.eval(a,b) else 'ERROR')
levenhtein_test()
