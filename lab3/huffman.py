class Node:
  def __init__(self,left,right,weight,sign=None):
    self.left=left
    self.right=right
    self.weight=weight
    self.sign=sign
def get_min(leafs,inner_nodes):
    if leafs and inner_nodes:
      return leafs.pop() if leafs[-1].weight<inner_nodes[-1].weight else inner_nodes.pop()
    elif leafs:
      return leafs.pop()
    elif inner_nodes:
      return inner_nodes.pop()
def static_huffman(letter_counts):
    nodes = []
    for a, weight in letter_counts.items():
        nodes.append(Node(left=None,right=None,sign=a, weight=weight))
    internal_nodes = [] 
    leafs = sorted(nodes, key=lambda n: -n.weight)
    for i in leafs:
      print(i.weight)
    while(len(leafs) + len(internal_nodes) > 1):
        element_1,element_2=get_min(leafs,internal_nodes),get_min(leafs,internal_nodes) 
        print(element_1.weight,element_2.weight)   
        internal_nodes.append(Node(element_1, element_2, element_1.weight + element_2.weight,None))
    return internal_nodes[0]
root=static_huffman({"a": 5, "b": 2, "c": 1, "d": 1, "r": 2})
def get_code(node, level=0):
    if node != None:
        get_code(node.left, level + 1)
        print(' ' * 4 * level + '->', node.weight,node.sign)
        get_code(node.right, level + 1)

get_code(root)