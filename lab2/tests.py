from suff_trie_with_compression import *
from trie import * 
from time import perf_counter
def check_correctnes(tree_build_f,factorin):
	for napis in text1,text2,text3,text4:
		root=tree_build_f(napis)
		for i in range(len(napis)):
			assert factorin(napis[i:],root.root)==True
		assert factorin(napis[len(napis)//2-2:len(napis)//2+2],root.root)==True,'should appear in text'
		assert factorin(napis[len(napis)//2-2:len(napis)//2+2]+'KKK',root.root)==False,'should not appear in text'
		assert factorin('ACT',root.root)==False,'should not appear in text'
		assert factorin('$',root.root)==True,'should appear in text'
def clock_measure(tree_build_f):
	for napis in text1,text2,text3,text4,load_text():
		t1=perf_counter()
		tree_build_f(napis)	
		t2=perf_counter()
		print('czas budowy drzewa trie dla',tree_build_f.__name__,'wyniosl',t2-t1)
check_correctnes(build_tree_schema_TRIE,trie_factorin)
check_correctnes(build_tree_schema_SUFF_TRIE,suff_factorin)
clock_measure(build_tree_schema_TRIE)
clock_measure(build_tree_schema_SUFF_TRIE)