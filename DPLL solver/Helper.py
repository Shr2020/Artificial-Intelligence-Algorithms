import re
import math as m

# open file and read
def read_file(file):
    setntence_list = []
    f = open(file, 'r')
    for x in f:
        first = x[0]
        if first == '#' or first == '\n':
            continue
        line_list = re.split(' |\t|\n', x.strip())
        i=0
        new_list= []
        while i < len(line_list):
            if line_list[i] != "!":
                new_list.append(line_list[i])
                i+=1
            else:
                if i+1 < len(line_list):
                    new_list.append(line_list[i] + line_list[i+1])
                    i+=2
                else:
                    new_list.append(line_list[i])
                    i=+1
        setntence_list.append(new_list)
    f.close()
    return (setntence_list)

def is_mode_valid(algo):
    if algo.lower() == "cnf":
        return True
    elif algo.lower() == "dpll":
        return True
    elif algo.lower() == "solver":
        return True
    return False

def is_bnf_text_valid(bnf):
    operators = ["<=>", "=>", "&", "|"]
    not_op = "!"

    for sentence in bnf:
        i = 0
        if sentence[len(sentence)-1] == not_op:
            return False
        if sentence[len(sentence)-1].endswith(not_op):
                return False
        if sentence[len(sentence)-1] in operators:
                return False
        for i in range(len(sentence)-1):
            if sentence[i].endswith(not_op):
                return False
            if sentence[i] in operators and sentence[i+1] in operators:
                return False
            if sentence[i].startswith(not_op):
                sent = sentence[i]
                sub = sent[1:]
                if sub.startswith(not_op):
                    return False
            if sentence[i].startswith(not_op):
                for op in operators:
                  if op in sentence[i]:
                    return False
    return True

def is_cnf_text_valid(cnf):
    not_op = "!"

    for sentence in cnf:
        i = 0
        if sentence[len(sentence)-1] == not_op:
            return False
        
        for i in range(len(sentence)):
            if sentence[i].endswith(not_op):
                return False
            if sentence[i].startswith(not_op):
                sent = sentence[i]
                sub = sent[1:]
                if sub.startswith(not_op):
                    return False
                if not sub.isalnum():
                    return False
            else:
                if not sentence[i].isalnum():
                    return False
    return True
