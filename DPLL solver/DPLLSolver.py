import BNFToCNF
import CNFToDPLL


def create_cnf_input(bnf_out):
    out_list = []
    for sentences in bnf_out:
        sent_list = sentences.split(" ")
        out_list.append(sent_list)
    return out_list


def solver(v, bnf):
    bnf_out = BNFToCNF.bnf_to_cnf(bnf)
    cnf_inp = create_cnf_input(bnf_out)
    CNFToDPLL.dpll(v, cnf_inp)

# b = ['P A B', 'P A C', '!Q A B', '!Q A C', '!W A B', '!W A C', '!P Q W !A', '!P Q W !B !C', '!A B', 'C B', 'C A']
# create_cnf_input(b)
