from collections import defaultdict
from bitarray import bitarray
from queue import Queue
class Node:
    def __init__(self,sign,weight,parent=None,index=-1):
        self.parent=parent
        self.weight=weight
        self.letter=sign
        self.index=index
        self.left=None
        self.right=None
    def code(self):
        tmp=self
        code=bitarray()
        while tmp.parent!=None:
            if tmp.parent.left==tmp:
                code.append(1)
            else:
                code.append(0)
            tmp=tmp.parent
        return code    
    def add_child(self,side,node):
        if side==0:
            self.left=node
        else:
            self.right=node
def swap(node1, node2):
        if node1 == node2 or node1.parent == node2 or node2.parent == node1:
            return
        if node1.parent==node2.parent:
            if node1.parent.left == node1:
                node1.parent.left = node2
                node1.parent.right = node1
            else:
                node1.parent.left = node1
                node1.parent.right = node2
            return
        node1_parent = node1.parent
        node2_parent = node2.parent
        if node1 == node1_parent.left:
            node1_parent.left = node2
        else:
            node1_parent.right = node2
        if node2 == node2_parent.left:
            node2_parent.left = node1
        else:
            node2_parent.right = node1
        node1.parent = node2_parent
        node2.parent = node1_parent

class adaptive_huffman:
    def __init__(self):
        self.codes={}
        self.root=self.NYT=Node('####',0)
        self.leaves={}
        self.nodes=[]
        self.codes={}
    def find_block_leader(self,node):
        indx=node.index-1
        while indx>=0 and self.nodes[indx].weight<node.weight:
            indx-=1#find last node from block
        return self.nodes[indx+1] if indx+1<len(self.nodes) else self.nodes[indx]#return it
    def update_indexes(self):
        self.nodes=[]
        q=Queue()
        q.put(self.root)
        indx=0
        while not q.empty():
            node=q.get()
            self.nodes.append(node)
            node.index=indx
            if node.right!=None:
                q.put(node.right)
            if node.left!=None:
                q.put(node.left)
            indx+=1
    def increment(self,node):
        while node!=None:
            node.weight+=1
            leader=self.find_block_leader(node)
            if leader!=node and leader!=node.parent and leader.parent!=node:
                swap(node,leader)
                self.update_indexes()
            node=node.parent
    def add_node(self,node):
        new_NYT=Node('####',0)
        node.parent=self.NYT
        new_NYT.parent=self.NYT
        self.NYT.left=new_NYT
        self.NYT.right=node
        self.NYT=new_NYT
    def print_tree(self,node):
        print(node.letter,node.weight,node.index)
        if node.left!=None:
            print('left kid of',node.letter,node.weight,node.index)
            self.print_tree(node.left)
        if node.right!=None:
            print('right kid of',node.letter,node.weight,node.index)
            self.print_tree(node.right)
    def adaptive_huffman(self,text):
        for letter in list(text):
            if letter in self.leaves:
                node = self.leaves[letter]
                self.increment(node)
            else:
                new_node=Node(letter,1)
                self.leaves[letter]=new_node
                self.add_node(new_node)
                parent=new_node.parent
                parent.index=len(self.nodes)
                self.nodes.append(parent)
                new_node.index=len(self.nodes)
                self.nodes.append(new_node)
                self.increment(parent)
        return self.root
    def get_code(self,root):
        if root.left!=None:
            self.get_code(root.left)
        if root.right!=None:
            self.get_code(root.right)
        if root.letter!='####':
            self.codes[root.letter]=root.code()[::-1]
    def generate_code(self,text):
        root=self.adaptive_huffman(text)
        self.get_code(self.root)
        return self.codes
