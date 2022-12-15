class Node:
    def __init__(self, data):
        self.left = None
        self.right = None
        self.negate = False
        self.data = data
        if data.startswith('!'):
            self.data = data[1:]
            self.negate = True

    def copy(self):
        copied = Node(self.data)
        copied.left = self.left
        copied.right = self.right
        copied.negate = self.negate
        return copied

    def to_string(self):
        s = "!" if self.negate else ""
        return s + self.data

operator_score = {'!': 4, '|': 2, '&': 3, "=>": 1, "<=>" : 0}
operators = ["!", "|", "&", "=>", "<=>"]

def find_lowest_score_operand(llist):
    score = 10
    index = -1
    length = len(llist)
    while length > 0:
        if operators.count(llist[length-1]) > 0:
            if operator_score[llist[length-1]] < score:
                score = operator_score[llist[length-1]]
                index = length - 1 
        length = length -1
    return (index, score)

def make_parse_tree(sentence):
    ind, score = find_lowest_score_operand(sentence)
    if len(sentence) == 0:
        return None
    if score == 10:
        assert len(sentence) == 1
        n = Node(sentence[0])
    if score < 10:
        # its a operator
        n = Node(sentence[ind])
        n.left = make_parse_tree(sentence[: ind])
        n.right = make_parse_tree(sentence[ind + 1: ])
    return n

# simplifies ALL "<=>" operators in tree rooted at node
# traverses the tree in a post-order fashion calling simplify_spaceship_at_node()
# whenever it finds a <=> operator
def simplify_spaceship(node):
    if node:
        node.left = simplify_spaceship(node.left)
        node.right = simplify_spaceship(node.right)

        if node.data == "<=>":
            simplified = simplify_spaceship_at_node(node)
            return simplified
    
    return node

# simplifies "<=>" operator at node
# a <=> b is simplified to (a => b) ^ (b => a)
def simplify_spaceship_at_node(node):
    assert node.data == "<=>"

    # a => b
    left = Node("=>")
    left.left = node.left   # a
    left.right = node.right # b

    # b => a
    right = Node("=>")
    right.left = copy_tree(node.right)  # we need to copy because node.right has been claimed by a => b
    right.right = copy_tree(node.left)

    simplified = Node("&")
    simplified.left = left
    simplified.right = right

    return simplified

def simplify_implies(node):
    if node:
        node.left = simplify_implies(node.left)
        node.right = simplify_implies(node.right)

        if node.data == "=>":
            simplified = simplify_implies_at_node(node)
            return simplified
    
    return node

# a => b is simplified as (NOT A) OR B
def simplify_implies_at_node(node):
    assert node.data == "=>"

    or_node = Node("|")
    or_node.left = node.left
    or_node.left.negate = not or_node.left.negate  # to implement NOT A
    or_node.right = node.right

    return or_node

def simplify_demorgan(node):
    if node is None:
        return None
    if node.negate == True:
        if node.data == "&":
            node = simplify_nand_demorgan_at_node(node)
        elif node.data == "|":
            node = simplify_nor_demorgan_at_node(node)
    
    node.left = simplify_demorgan(node.left)
    node.right = simplify_demorgan(node.right)
    return node

# NOT(a OR b) is simplified to NOT(a) AND NOT(b)
def simplify_nor_demorgan_at_node(node):
    assert node.data == "|"
    assert node.negate == True

    # convert node from NOR to AND and negate the children
    node.data = "&"
    node.negate = False
    node.left.negate = not node.left.negate
    node.right.negate = not node.right.negate

    return node

def simplify_nand_demorgan_at_node(node):
    assert node.data == "&"
    assert node.negate == True

    # convert node from NAND to OR and negate the children
    node.data = "|"
    node.negate = False
    node.left.negate = not node.left.negate
    node.right.negate = not node.right.negate

    return node

def need_distribute(node):
    if node:
        if node.data == "|" and (node.left.data == "&" or node.right.data == "&"):
            return True
        else:
            return need_distribute(node.left) or need_distribute(node.right)
    return False

def distribute(node):
    if node is None:
        return None
    if node.data == "|" and (node.left.data == "&" or node.right.data == "&"):
        node = distribute_at_node(node)

    node.left = distribute(node.left)
    node.right = distribute(node.right)
    return node

def distribute_at_node(node):
    assert node.data == "|" and (node.left.data == "&" or node.right.data == "&")

    if node.right.data == "&":
        inner_and = node.right
        other_child = node.left
    else:
        inner_and = node.left
        other_child = node.right

    top_and = Node("&")
    top_and.left = Node("|")
    top_and.right = Node("|")

    top_and.left.left = other_child
    top_and.left.right = inner_and.left
    top_and.right.left = copy_tree(other_child)
    top_and.right.right = inner_and.right
    
    return top_and

def copy_tree(node):
    if node:
        copied_node = node.copy()
        copied_node.left = copy_tree(node.left)
        copied_node.right = copy_tree(node.right)

        return copied_node
    return None

def to_cnf(node):
    cnf = ""
    if node:
        assert node.data not in ['=>', '<=>', '!'], "{}".format(node.data)

        left_cnf = to_cnf(node.left)
        right_cnf = to_cnf(node.right)

        if node.data == "|":
            assert node.negate == False
            assert node.left.data not in operators or node.left.data == "|", "{}".format(node.left.data)
            assert node.right.data not in operators or node.right.data == "|", "{}".format(node.right.data)
            
            cnf = left_cnf + " " + right_cnf

        elif node.data == "&":
            assert node.negate == False
            assert node.left.data not in operators or node.left.data in ["|", "&"]
            assert node.right.data not in operators or node.right.data in ["|", "&"]

            cnf = left_cnf + "," + right_cnf

        else:
            assert node.data not in operators
            cnf = node.to_string()

    return cnf

def bnf_to_cnf(sentences):
    cnf = []
    print("BNF To CNF:")
    print()
    for sentence in sentences:
        tree = make_parse_tree(sentence)
        tree = simplify_spaceship(tree)
        tree = simplify_implies(tree)
        tree = simplify_demorgan(tree)
        while need_distribute(tree):
            tree = distribute(tree)
        cnf_inner = to_cnf(tree).split(",")
        cnf.extend(cnf_inner)
    for c in cnf:
        print(c)
    print()
    return cnf
