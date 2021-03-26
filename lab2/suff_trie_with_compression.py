from text_load import *
from os.path import commonprefix
def print_trie(node,sign):
	print('jestem na glebokosci ',node.node_depth)
	if(sign==special_sign):
		return
	for s in list(node.kids.keys()):
		print(s,sep=' ',end= ' ')
	print('\n')
	for s in list(node.kids.keys()):
		print('wchodze z ',s)
		print_trie(node.kids[s],s)
class Node():
	def __init__(self):
		self.kids={}
		self.node_depth=0
	def depth(self):
		return self.node_depth
	def graft(self,text):
		tmp=Node()
		tmp.node_depth=self.node_depth+len(text)
		self.kids[text]=tmp
class Trie():
	def __init__(self,trie_root):
		self.root=trie_root
	def leafs(self):
		return list(self.root.kids.items())
	def find(self,x,leaf):
		"""return node to which text or part of it should be grafted
			insert new node if needed"""
		node=self.root
		while len(node.kids.keys())!=0:
			for s in list(node.kids.keys()):
				pref=commonprefix([s,x])
				if pref!='':
					if node.kids.get(pref)!=None:
						node=node.kids.get(pref)
						x=x[len(pref):]
						break
					mid=Node()
					leaf=node.kids[s]
					mid.kids[s[len(pref):]]=leaf
					mid.node_depth=node.node_depth+len(pref)
					leaf.node_depth=mid.node_depth+len(s[len(pref):])
					node.kids[pref]=mid
					node.kids.pop(s)
					x=x[len(pref):]
					node=mid
					break
			else:
				return node
def compute_initial_trie(text):
	root=Node()
	leaf=Node()
	root.kids[text]=leaf
	return Trie(root)
def suff_factorin(x,T):
	node=T
	while len(node.kids.keys())!=0:
		for s in list(node.kids.keys()):
			pref=commonprefix([s,x])
			if pref!='':
				node=node.kids[s]
				x=x[len(pref):]
				if len(x)==0:
					return True
				break
		else:
			return False
	return False
def build_tree_schema_SUFF_TRIE(text):
    trie = compute_initial_trie(text)
    leaf = trie.leafs()[0]
    for i in range(1, len(text)):
        suffix = text[i:]
        # print('suf=',suffix)
        head = trie.find(suffix, leaf)
        suffix_end = suffix[head.depth():]
        # print(trie.root.kids.keys())
        # print('dolaczam do ',head.kids.keys(),suffix_end)
        leaf = head.graft(suffix_end)
    return trie
