
global verbose

def set_all_atoms_in_dict(cnf_set):
    atom_dict = {}
    total_atoms = 0
    i = 0
    for sent_list in cnf_set:
        for at in sent_list:
            atom = remove_negation(at)
            if not atom in atom_dict.keys():
                # atom not yet in list
                atom_dict[atom] = i
                i+=1
    total_atoms = i
    
    # order atoms
    j=0
    for atom in sorted(atom_dict.keys()):
        atom_dict[atom] = j
        j+=1
    return (atom_dict, total_atoms)

def set_atoms_to_unset(total_atoms):
    atoms = []
    for i in range(total_atoms):
        atoms.append(-1)
    return atoms

def remove_negation(atom):
    if atom.startswith("!"):
        return atom[1:]
    else:
        return atom

def get_val(i):
    if i == 0:
        return False
    else:
        return True

def handle_unbounded_atoms(atoms, atom_dict):
    for atom, ind in atom_dict.items(): 
        if atoms[ind] == -1:
            print("Unbounded: ", atom)
            atoms[ind] = 0
    return atoms

def print_formula(atoms, atom_dict):
    for atom in sorted(atom_dict):
        if (atoms[atom_dict[atom]] == 1):
            print(atom, "=", True)
        else:
            print(atom, "=", False)

def get_index_in_dict(atom_dict, literal):
     atom = remove_negation(literal)
     return atom_dict[atom]

def get_value_literal(atom_val, literal):
    if literal.startswith("!"):
        if atom_val == 1:
            return 0
        elif atom_val == 0:
            return 1
        else:
            return -1
    else:
        if atom_val == 0:
            return 0
        elif atom_val == 1:
            return 1
        else:
            return -1

def calculate_value(val1, val2):
    if val2 == -1 and val1 == 0:
        return -1
    elif val2 == -1 and val1 == 1:
        return 1
    elif val2 == 0 and val1 == 1:
        return 1
    elif val2 == 0 and val1 == -1:
        return -1
    elif val2 == 1 and val1 == 0:
        return 1
    elif val2 == 1 and val1 == -1:
        return 1
    elif val2 == 0 and val1 == 0:
        return 0
    elif val2 == 1 and val1 == 1:
        return 1
    elif val2 == -1 and val1 == -1:
        return -1

def get_values_cnf_sentences(atoms, cnf_set, atom_dict):
    # returns the value of each sentence in cnf_set. 0 = false, 1 = true, -1 = not set yet
    values_cnf =  []
    for l_sent in cnf_set:
        value_so_far_per_sentence = 0
        for literal in l_sent:
            ind = get_index_in_dict(atom_dict, literal)
            val = get_value_literal(atoms[ind], literal)
            value_so_far_per_sentence = calculate_value(value_so_far_per_sentence, val)
        values_cnf.append(value_so_far_per_sentence)
    return values_cnf

def check(atoms, cnf_set, atom_dict):
    
    values_cnf = get_values_cnf_sentences(atoms, cnf_set, atom_dict)

    if values_cnf.count(-1) == 0:
        # all statements have values
        cnf_all_set = 1
    else:
        # some statements do not have a valuue 
        cnf_all_set = 0

    if  values_cnf.count(0) != 0: 
        #  at least one of statements is false. check failed
        cnf_all_set = 0  # set to zero since this solution not acceptable
        return False, cnf_all_set
    else:
        # either statements are true or some of the literals are still unset
        return True, cnf_all_set    

def get_single_literals(atoms, atom_dict, cnf_set):
    #create dict for pure literals
    
    values_cnf = get_values_cnf_sentences(atoms, cnf_set, atom_dict)

    #[(p:0), (q:1)] atom and its form positive or negative
    single_occurence= []
    i = 0
    for l_sent in cnf_set:
        if (values_cnf[i] == -1):
            num_unset_literal = 0
            unset_atom = ""
            for literal in l_sent:
                abs_literal = remove_negation(literal)
                if atoms[atom_dict[abs_literal]] == -1:
                    num_unset_literal +=1
                    unset_atom = literal
            if num_unset_literal == 1:
                #single occurence found
                val = -1
                if unset_atom.startswith("!"):
                    val = 0
                else:
                    val = 1
                single_occurence.append((remove_negation(unset_atom), val))
                break
        if (len(single_occurence) != 0):
            break
        i+=1
        
    if len(single_occurence) == 0:
        return (-1, -1)
    else:
        # returns a tuple of atom and its val
        return (single_occurence[0][0], single_occurence[0][1])

def get_pure_literals(atoms, atom_dict, cnf_set):

    # {p:1, q:0} . p is present as p in cnf. q is pure literal presnt as !q in cnf
    atom_pure_dict = {}
    i = 0
    values_cnf = get_values_cnf_sentences(atoms, cnf_set, atom_dict)
    for atom, ind in atom_dict.items():
        if atoms[ind] != -1:
            continue
        forms=[]
        i = 0
        for l_sent in cnf_set:
            if (values_cnf[i] == -1):
                for literal in l_sent:
                    abs_literal = remove_negation(literal)
                    if atom == abs_literal:
                        if literal.startswith('!'):
                            forms.append(0)
                        else:
                            forms.append(1)
            i+=1
        if (len(forms) > 0):
            if not (forms.count(0) > 0 and forms.count(1) > 0):
                atom_pure_dict[atom] = (forms[0])

    pure_literal = []
    for atom, val in atom_pure_dict.items():
        if len(pure_literal) == 0:
            pure_literal.append((atom, val))

    if len(pure_literal) != 0:
        # returns a tuple of atom and its val
        return pure_literal[0]
    else:
        return (-1, -1)

def dpll_helper(start, end, atom_dict, atoms, cnf_all_set, cnf_set):
    if cnf_all_set == 1 or start == end:
        atoms = handle_unbounded_atoms(atoms, atom_dict)
        print_formula(atoms, atom_dict)
        return True
    
    easy_case_indexes = []
   
    single_lit_case_exist = True
    pure_lit_case_exist = True
    
    while(single_lit_case_exist):
        at, val = get_single_literals(atoms, atom_dict, cnf_set)
        if (at != -1):
            ind_atom = atom_dict[at]
            if (atoms[ind_atom] != -1):
                if(verbose):
                    print("Something wrong")
            else:
                atoms[ind_atom] = val
                easy_case_indexes.append((at, ind_atom))
                if(verbose):
                    print("Easy case:", at, "val:", get_val(val))
                    print_cnf(atom_dict, atoms, cnf_set)
        else:
            single_lit_case_exist = False

    cnf_values = get_values_cnf_sentences(atoms, cnf_set, atom_dict)
    if cnf_values.count(0) == 0 and cnf_values.count(-1) == 0:
        print_cnf(atom_dict, atoms, cnf_set)
        atoms = handle_unbounded_atoms(atoms, atom_dict)
        print_formula(atoms, atom_dict)
        return True
    
    while(pure_lit_case_exist):
        at, val = get_pure_literals(atoms, atom_dict, cnf_set)
        if (at != -1):
            
            ind_atom = atom_dict[at]
            if (atoms[ind_atom] != -1):
                if(verbose):
                    print("Something wrong")
            else:
                atoms[ind_atom] = val
                easy_case_indexes.append((at, ind_atom))
                if(verbose):
                    print("Easy case:", at, "val:", get_val(val))
                    print_cnf(atom_dict, atoms, cnf_set)
        else:
            pure_lit_case_exist = False
    
    cnf_values = get_values_cnf_sentences(atoms, cnf_set, atom_dict)
    if cnf_values.count(0) == 0 and cnf_values.count(-1) == 0:
        print_cnf(atom_dict, atoms, cnf_set)
        atoms = handle_unbounded_atoms(atoms, atom_dict)
        print_formula(atoms, atom_dict)
        return True

    for i in range(start, end):
        if (atoms[i] != -1):
            continue
        else:
            atom_name = ""
            for atom, ind in atom_dict.items():
                if ind == i:
                    atom_name= atom
            
            
            atoms[i] = 1
            if(verbose):
                print("Hard Case:", atom_name, "val: True")
                print_cnf(atom_dict, atoms, cnf_set)
            
            isSafe, cnf_all_set_val = check(atoms, cnf_set, atom_dict)
            if (isSafe and dpll_helper(i+1, end, atom_dict, atoms, cnf_all_set_val, cnf_set)):
                return True
            
            if(verbose):
                print("Failed. Choose another branch.")
                print("Hard Case:", atom_name, "val: False")
                print_cnf(atom_dict, atoms, cnf_set)
            atoms[i] = 0
            isSafe, cnf_all_set_val = check(atoms, cnf_set, atom_dict)
            if (isSafe and dpll_helper(i+1, end, atom_dict, atoms, cnf_all_set_val, cnf_set)):
                return True

            if(verbose):
                print("Failed. Choose another branch.")
            atoms[i] = -1
            break
    
    for at, ind in easy_case_indexes:
        atoms[ind] = -1
    return False

def print_cnf(atoms_dict, atoms, cnf_set):
    cnf_values = get_values_cnf_sentences(atoms, cnf_set, atoms_dict)
    i = 0
    for sentence in cnf_set:
        s = ""
        empty_string = True
        if cnf_values[i] == -1:
            for literal in sentence:
                abs_lit = remove_negation(literal)
                if atoms[atoms_dict[abs_lit]] == -1:
                    s = s + literal + " " 
                    empty_string = False
            if not empty_string:
                print(s)
        i+=1
    print()


def dpll(v, cnf):
    global verbose
    verbose = v
    print()
    print("CNF in DPLL Solver:")
    print()
    # cnf_set contains all sentences in cnf (sentences in list form) in list
    cnf_set = cnf

    #atom_dict = contains dictionary that maps atom to indexes in atoms list. eg. {0:a, 1:p..}
    atom_dict, total_atoms = set_all_atoms_in_dict(cnf_set)
    
    # list of atoms (atom looks like P, q, a v, They are in absolute form (without negation))
    atoms = set_atoms_to_unset(total_atoms)

    # boolean 0 or 1. 1 if all statements are True or false. 0 if some statements still remains
    cnf_all_set = 0

    if verbose:
        print_cnf(atom_dict, atoms, cnf_set)

    s = dpll_helper(0, total_atoms, atom_dict, atoms, cnf_all_set, cnf_set)
    if not s:
        print("No Solution Found")




