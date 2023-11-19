
from database import *


class Variable :
    def __init__(self, val) :
        self.val = val

    def __str__(self) :        
        return self.val

    def __eq__(self, another) :
        if isinstance(another, Variable) :
            return self.val == another.val
        return False



class RelAtom:
    ''' R[A, B] R(x1, x2)'''
    rel_name : Relation


    def __init__(self, relation, list_vars):
        self.rel_name = relation
        self.list_vars = list_vars
        self.list_attr = list()             #TODO make assert nb vars = nb attributes
        

    def __str__(self):
              
        ret = str(self.rel_name) + '('        
   
        for el in self.list_vars:       #TODO do we really need list of list ?
            for v in el:
                ret += str(v) + ', '        
            ret = ret[:-2]
            ret += ')'

        return ret
    
    def __iter__(self) :
        self.index = 0
        return self
    
    def __next__(self) :
        if self.index < len(self.list_vars) :
            result = self.list_vars[self.index]
            self.index += 1
            return result
        else :
            raise StopIteration

    def get_index_var(self, var):
        index = -1
        try:
            index = self.list_vars[0].index(var)
            return index
        except Exception as e:
           # print('variable ' + str(var) + ' is not in relation atom ' + str(self.rel_name))
            return index


    

class EqAtom:
    ''' x1 = x2'''
    whoIsEqual : Variable
    toWhom : list 
    
    def __init__(self, at1, at2):
        self.whoIsEqual = at1
        self.toWhom = at2           # can be variable or EqAtom

    def __str__(self):  
        ret = str(self.whoIsEqual)      
        for e in self.toWhom :
            ret = ret + "=" + str(e)
        # return str(self.whoIsEqual) + '=' + str(self.toWhom)
        return ret



class AtomConj :
    ''' R(x1, y1) /\ Q(y2, x2) /\ x1 = y1 '''
    list_atom = []

    def __init__(self, list_atom) :
        self.list_atom = list_atom

    def __iter__(self) :
        self.index = 0
        return self

    def __next__(self) :
        if self.index < len(self.list_atom) :
            result = self.list_atom[self.index]
            self.index += 1
            return result
        else :
            raise StopIteration
    
    def __str__(self):
        ret = ''
        for el in self.list_atom:
            ret += str(el) + ' and '
        ret = ret[:-5]
        return ret
       
    def get_EqAtom(self):                       # TODO if multiple EqAtom in this AtomConj ?
        for el in self.list_atom:
            if isinstance(el, EqAtom):
                return el
      #  print('this AtomConj ' + str(self) + ' has not EqAtom')
        return None

class Instruction :
    fromRel: Relation
    fromAttr: int
    toRel: Relation
    toAttr: int

    def __init__(self, fromR, fromA, toR, toA) :
        self.fromRel = fromR      
        self.fromAttr = fromA    
        self.toRel = toR      
        self.toAttr = toA  

    def __str__(self):
        return '[' + str( self.fromRel) + ', ' + str(self.fromAttr) + ', ' +  str(self.toRel) + ', ' + str(self.toAttr) + ']'


class InstructionEGD :
    def __init__(self, list_instr_IF, list_instr_THEN) :
        self.ifEq = list_instr_IF     
        self.thenEq = list_instr_THEN    
  
    def __str__(self):

        ret = 'if '

        for inst in self.ifEq:
            ret += str(inst) + ', '
        ret = ret[:-2]

        ret += ' then '

        for inst in self.thenEq:
            ret += str(inst) + ', '
        ret = ret[:-2]

        return ret
    
    def get_ifEq(self) :
        return self.ifEq
  
    def get_thenEq(self) :
        return self.thenEq
    


class DF :
    left : AtomConj # corps
    right : AtomConj # tete

    def __init__(self, left, right) :
        self.left = left
        self.right = right
        

    def __str__(self):        
        return str(self.left) + '  -> '+ str(self.right)


    def complete_attributes(self, database):
        for el in self.left.list_atom:
            if isinstance(el, RelAtom):                
                el.list_attr = el.list_attr + database.find_table_by_relation(el.rel_name).attr_list
        
        for el in self.right.list_atom:
            if isinstance(el, RelAtom):                
                el.list_attr = el.list_attr + database.find_table_by_relation(el.rel_name).attr_list

    
    def is_TGD(self) :
        corps = self.left
        tete = self.right
        if len(corps.list_atom) != 1 :
            print("corps a plus d'un atome")
            return False
        for atom in corps.list_atom :
            if isinstance(atom, EqAtom) :
                print("contient EqAtom")
                return False
        for atom in tete.list_atom :
            if isinstance(atom, EqAtom) :
                print("contient EqAtom")
                return False
        list_vars = corps.list_atom[0].list_vars[0]
        
        same_var = 0
        diff_var = 0
        
        for atom in tete.list_atom :
            for var in atom.list_vars[0] :
                if var in list_vars :
                    same_var += 1
                else :
                    diff_var += 1
            if same_var == 0 or diff_var == 0 :
                return False
        return True

    
    def is_EGD(self):
        leftEq = self.left.get_EqAtom()
        rightEq = self.right.get_EqAtom() 
        if rightEq == None : 
            print('\nThis DF ' + str(self) + ' is not EGD\n')
            return False
        isEGD = False
        for atom in self.left.list_atom:
            if isinstance(atom, RelAtom):                
                if ( atom.get_index_var(rightEq.whoIsEqual) != -1 ):                    
                    isEGD = True                    
        
                for vars in rightEq.toWhom:      # toWhom  can be list                    
                    if ( atom.get_index_var(vars) != -1 ):  
                        isEGD = True                    
        
        if not isEGD:            
            print('\nThis DF ' + str(self) + ' is not EGD\n')
     
        return isEGD

    def create_instructions_TGD(self):
        body = self.left.list_atom
        head = self.right.list_atom
        def make_job(atomTo, atomFrom):
            listInstr = list()
            for i in range(len(atomFrom.list_vars[0])):
                for j in range(len(atomTo.list_vars[0])):
                    if atomFrom.list_vars[0][i] == atomTo.list_vars[0][j]:                   
                        listInstr.append( Instruction(atomFrom.rel_name, i, atomTo.rel_name, j) )
            return listInstr

        allInstr = []
        for relTo in head:
            newInstr = []
            for relFrom in body:
                newInstr.append( make_job(relTo, relFrom) )               
            allInstr = allInstr + newInstr
        return allInstr


    def create_instructions_EGD(self):
        
        # REFERENCE: InstructionEGD(list_instrIf, list_instrThen)        
        listInsuctionsIF = []
        listInstructionsThen = []

        leftEquality = self.left.get_EqAtom()                   # TODO what if left AtomConj has multiple EqAtom ? 

        body = self.left.list_atom
        for atom in body:
            if isinstance(atom, RelAtom):       
                index = atom.get_index_var(leftEquality.whoIsEqual)
                
                if ( index != -1):
                    ifEqInstruction = Instruction(None, -1, None, -1)
                    ifEqInstruction.fromRel = atom.rel_name
                    ifEqInstruction.fromAttr = index
                
                for vars in leftEquality.toWhom:      # toWhom  can be list
                    index = atom.get_index_var(vars)
                    if ( index != -1 ):  
                        ifEqInstruction.toRel = atom.rel_name
                        ifEqInstruction.toAttr = index
                        listInsuctionsIF.append(ifEqInstruction)

        rightEquality = self.right.get_EqAtom()                  # TODO what if right AtomConj has multiple EqAtom ?       

        head = self.right.list_atom
        for atom in body:
            if isinstance(atom, RelAtom):       
                index = atom.get_index_var(rightEquality.whoIsEqual)
                if ( index != -1):
                    thenEqInstruction = Instruction(None, -1, None, -1)
                    thenEqInstruction.fromRel = atom.rel_name
                    thenEqInstruction.fromAttr = index
                
                for vars in rightEquality.toWhom:      # toWhom  can be list
                    index = atom.get_index_var(vars)
                    if ( index != -1 ):  
                        thenEqInstruction.toRel = atom.rel_name
                        thenEqInstruction.toAttr = index
                        listInstructionsThen.append(thenEqInstruction)
                
        return InstructionEGD(listInsuctionsIF, listInstructionsThen)
