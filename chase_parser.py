from parsimonious.grammar import Grammar
from parsimonious.nodes import NodeVisitor
from contraintes import *
from database import *



def get_grammar():
    return Grammar(
        r"""
        df = conjatom implies ws+ conjatom
        conjatom = atomList+
        atomList = (atom ws+ and ws+) / (atom ws*)
        atom = relAtom / eqAtom
        relAtom = relation tuples
        eqAtom = eqVar+
        eqVar = (variable equals ws*) / (equals? ws* variable)
        relation = ~"[A-Z]+[a-z]*"
        tuples = "(" variableList+ ")"
        variableList = (variable comma) / (comma? variable)
        variable = ~"[a-z]+[0-9]*"      
        comma = ","
        implies = "->"
        equals = "="
        and = "and"
        ws = ~"[^\S\r\n]"
        """
        )

def parcours_liste(l, type, ret) :
    for i in l :
        if isinstance(i, list) :
            parcours_liste(i, type, ret)
        if isinstance(i, type) :
            ret.append(i)
    return ret
    

class DFParser(NodeVisitor) :        
        
    def visit_variable(self, node, vc) :
        return Variable(node.text)

    def visit_df(self, node, vc) :
        left : AtomConj
        right : AtomConj
        implied = False
        
        for child in vc :
           
            if isinstance(child, AtomConj) :
                if implied :
                    right = child
                else :
                    left = child
            elif isinstance(child, list) :
                pass
            else :
                implied = True
        return DF(left, right)

    def visit_conjatom(self, node, vc) :
        ret = []
        for child in vc :
            ret.append(child[0])
        return AtomConj(ret)

    def visit_atomList(self, node, vc): 
        ret = []
        for child in vc : 
            parcours_liste(child, RelAtom, ret)
            parcours_liste(child, EqAtom, ret)
        return ret

    def visit_atom(self, node, vc) :
        ret = []
        for child in vc :
            ret.append(child)
        return ret

    def visit_eqVar(self, node, vc) :
        ret = []
        
        for child in vc :
            parcours_liste(child, Variable, ret)
        
        return ret

    def visit_eqAtom(self, node, vc) :
        ret = []
        for i in range(1,len(vc)) :
            if isinstance(vc[i][0], Variable):
                ret.append(vc[i][0]) 
        return EqAtom(vc[0][0], ret)
    
    def visit_variableList(self, node, vc) :
        ret = []
        for child in vc :
            parcours_liste(child, Variable, ret)
        return ret

    def visit_relation(self, node, vc) :
        return Relation(node.text)

    def visit_tuples(self, node, vc) :
        ret = []
        for child in vc :
            if isinstance(child, list):
                ret.append([item for sublist in child for item in sublist])
        return ret

    
    def visit_relAtom(self, node, vc) :
        relation, tuples = vc
        return RelAtom(relation, tuples)

    def generic_visit(self, node, visited_children) :
        return visited_children or node