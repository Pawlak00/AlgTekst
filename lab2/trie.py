from text_load import *
def print_trie(node,sign):
	print('jestem na glebokosci ',node.node_depth)
	if(sign==special_sign):
		return
	for s in list(node.kids.keys()):
		print(s,sep=' ',end= ' ')
	print('\n')
	for s in list(node.kids.keys()):
		print_trie(node.kids[s],s)
class Node():
	def __init__(self):
		self.kids={}
		self.node_depth=0
	def depth(self):
		return self.node_depth
	def graft(self,text):
		last=self
		for s in text:
			new_node=Node()
			new_node.node_depth=last.node_depth+1
			last.kids[s]=new_node
			last=new_node
class Trie():
	def __init__(self,trie_root):
		self.root=trie_root
	def leafs(self):
		next_node=self.root
		while list(next_node.kids.keys())[0]!=special_sign:
			next_node=next_node.kids[list(next_node.kids.keys())[0]]
		return [next_node]
	def find(self,suffix,leaf):
		node=self.root
		pos=0
		while suffix[pos] in node.kids.keys():
			node=node.kids[suffix[pos]]
			pos+=1
		return node 
def compute_initial_trie(text):
	i=0
	root=Node()
	last=root
	while i<len(text):
		curr_leaf=Node()
		last.kids[text[i]]=curr_leaf
		curr_leaf.node_depth=last.node_depth+1
		last=curr_leaf
		i+=1
	return Trie(root)
def trie_factorin(x,T):
	pos=0
	curr=T
	while pos<len(x) and x[pos] in curr.kids.keys():
		curr=curr.kids[x[pos]]
		pos+=1
	if pos==len(x):
		return True
	return False
def build_tree_schema_TRIE(text):
    trie = compute_initial_trie(text)
    leaf = trie.leafs()[0]
    for i in range(1, len(text)):
        suffix = text[i:]
        head = trie.find(suffix, leaf)
        suffix_end = suffix[head.depth():]
        leaf = head.graft(suffix_end)
    return trie
