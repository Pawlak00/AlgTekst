from bitarray import bitarray
from queue import PriorityQueue
class Node:
  def __init__(self,weight,sign,left,right):
    self.left=left
    self.right=right
    self.weight=weight
    self.sign=sign
class static_huffman:
	def __init__(self):
		self.codes={}
	def static_huffman_alg(self,letter_counts):	
		pq=PriorityQueue()
		nodes=[Node(s[0],s[1],None,None) for s in letter_counts]
		nodes.sort(key=lambda x:x.weight,reverse=True)
		# print(nodes[0].weight,nodes[1].weight,nodes[20].weight)
		while len(nodes)>1:
			p,q=nodes.pop(),nodes.pop()
			# print(p.weight,q.weight)
			new_node=Node(p.weight+q.weight,p.sign+q.sign,p,q)
			nodes.append(new_node)
			nodes.sort(key=lambda x:x.weight,reverse=True)
		return nodes.pop()
	def get_code(self,node, level=0,code=bitarray()):
		if node != None:
			if node.sign!=None and len(node.sign)==1:
				self.codes[node.sign ]=code
			code_r=code.copy()
			code_l=code.copy()
			code_r.append(0)
			code_l.append(1)    
			self.get_code(node.left, level + 1,code=code_l)
			self.get_code(node.right, level + 1,code=code_r)
	def generate_code(self,text):
		sign_count={}
		for sign in text:
			if sign in sign_count:
				sign_count[sign]=sign_count[sign]+1
			else:
				sign_count[sign]=1
		sign_count=[(sign_count[sign],sign) for sign in sign_count]
		# print(sign_count)
		root=self.static_huffman_alg(sign_count)
		# print('root=',root.sign,root.weight)
		self.get_code(root,code=bitarray())
		# print(self.codes)
		return self.codes
