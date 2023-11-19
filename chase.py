import chase_parser as chp
from contraintes import *
from database import *


class NoneObj:    
    def __init__(self, val) :
        self.val = val

    def __str__(self):        
        return 'None' + str(self.val)

    def __eq__(self, other) :
        if isinstance(other, NoneObj) :
            return self.val == other.val
        return False 


def satisfaitCorps(df, table) : # database au lieu de table
    corps = df.left
    corps_tuples = corps.list_atom
    table_tuples = table.table
    satisfies = True
    for atom in corps_tuples :
        for k in range(0, table.key) :
            if table_tuples[k] == [] :
                return True
            satisfies = True
            if len(table_tuples[k] != len(atom.list_vars[0])) :
                satisfies = False
            else :
                for i in range(0, len(table_tuples[k])) :
                    for j in range(i+1, len(table_tuples[k])) :
                        if table_tuples[k][i] == table_tuples[k][j] :
                            if atom.list_vars[0][i] != atom.list_vars[0][j] :
                                satisfies = False
                        elif table_tuples[k][i] != table_tuples[k][j] :
                            if atom.list_vars[0][i] == atom.list_vars[0][j] :
                                satisfies = False
                if satisfies == True : # au moins une ligne qui satisfait
                    return True

    return satisfies

def create_instructions(str_dfs, database):
    instructions = []

    for text in str_dfs.splitlines() :
        tree = chp.get_grammar().match(text)
        res = chp.DFParser()
        output = res.visit(tree) 
        output.complete_attributes(database)        
        print(output)

        if (output.is_TGD()):
            instructions = instructions + output.create_instructions_TGD()

        elif(output.is_EGD()) :
            instructions = instructions + [output.create_instructions_EGD()]

    return instructions


def apply_TGD(list_instr, database: DataBase):

    for instr in list_instr:
        if (len(instr) == 1):

            print('Instruction : ' + str(instr[0]))
            tableFrom = database.find_table_by_relation(instr[0].fromRel)
            tableTo = database.find_table_by_relation(instr[0].toRel)
            columnFrom = instr[0].fromAttr        
            columnTo = instr[0].toAttr
            count = 1

            for i in range(1, len(tableFrom.table) + 1):
                isFound = False
                for j in range(1, len(tableTo.table) + 1):
                    if ( tableFrom.table[i][columnFrom] == tableTo.table[j][columnTo] ):                   
                        isFound = True
                        break

                if not isFound:
                    nbCol = tableTo.nb_columns
                    newItem = []              
    
                    for k in range(0, nbCol):
                        count += 1
                        if columnTo == k:                        
                            newItem.append(tableFrom.table[i][columnFrom])
    
                        else:
                            newItem.append(NoneObj(count - i))
    
                    tableTo.insert(newItem)    
            print('Modified table :')
            print(tableTo)

        
        else: # list of instructions on the same relations  -> need to merge results
            resInstructions = []

            for inst in instr:
                isFound = False
                print('Instruction : ' + str(inst))
                tableFrom = database.find_table_by_relation(inst.fromRel)
                tableTo = database.find_table_by_relation(inst.toRel)
                columnFrom = inst.fromAttr        
                columnTo = inst.toAttr
                count = 1

                for i in range(1, len(tableFrom.table) + 1):
                   # isFound = True
                    for j in range(1, len(tableTo.table) + 1):
                        if ( tableFrom.table[i][columnFrom] == tableTo.table[j][columnTo] ):  
                            isFound = isFound and True
                            break

                    if not isFound:
                        isFound = isFound and False
                        nbCol = tableTo.nb_columns
                        newItem = []              

                        for k in range(0, nbCol):
                            count += 1
                            if columnTo == k:                        
                                newItem.append(tableFrom.table[i][columnFrom])

                            else:
                                newItem.append(NoneObj(count - i))
                        
                        resInstructions.append(newItem)
                       

            chunks = [resInstructions[i:i + len(instr)] for i in range(0, len(resInstructions), len(instr))]
            
            for i in range(len(chunks[0])):
                toInsert = [NoneObj(i)]*len(chunks[0][0])
                for j in range(len(chunks)):                    
                    for k in range(len(resInstructions[0])):
                        if not isinstance(chunks[j][i][k], NoneObj):                                     
                            toInsert[k] = chunks[j][i][k]
                
                tableTo.insert(toInsert)
            print('Modified table :')
            print(tableTo)





def apply_EGD(instr_EGD: InstructionEGD, database: DataBase):

    if 0 == len(instr_EGD):
        return
    
    print('\nInstruction EGD : ' + str(instr_EGD[0]) + '\n\n')

    '''
    parcourir r 
        parcourir p
            si r[1] == p[0]
                r[0] = p[1]
    '''
    list_if = instr_EGD[0].get_ifEq()[0]
    list_then = instr_EGD[0].get_thenEq()[0]
    tableIfFrom = database.find_table_by_relation(list_if.fromRel)
    tableIfTo = database.find_table_by_relation(list_if.toRel)
    columnIfFrom = list_if.fromAttr        
    columnIfTo = list_if.toAttr

    tableThenFrom = database.find_table_by_relation(list_then.fromRel)
    tableThenTo = database.find_table_by_relation(list_then.toRel)
    columnThenFrom = list_then.fromAttr
    columnThenTo = list_then.toAttr

    for i in range(1, len(tableIfFrom.table)+1) :
        for j in range(1, len(tableIfTo.table)+1) :
            if(tableIfFrom.table[i][columnIfFrom] == tableIfTo.table[j][columnIfTo]) :
                tmpTo = tableThenTo.table[j][columnThenTo]
                tmpFrom = tableThenFrom.table[i][columnThenFrom]
                if not isinstance(tableThenTo.table[j][columnThenTo], NoneObj) :
                    tableThenFrom.table[i][columnThenFrom] = tableThenTo.table[j][columnThenTo]
                else :
                    tableThenTo.table[j][columnThenTo] = tableThenFrom.table[i][columnThenFrom] 
                # egalisation de toutes les variables
                if isinstance(tmpTo, NoneObj) :
                    for u in range(1, len(tableThenTo.table)+1) :
                        for v in range(0, tableThenTo.nb_columns) :
                            if isinstance(tableThenTo.table[u][v], NoneObj) and  tableThenTo.table[u][v] == tmpTo :
                                tableThenTo.table[u][v] = tmpTo
                if isinstance(tmpFrom, NoneObj) :
                    for u in range(1, len(tableThenFrom.table)+1) :
                        for v in range(0, tableThenFrom.nb_columns) :
                            if isinstance(tableThenFrom.table[u][v], NoneObj) and  tableThenFrom.table[u][v] == tmpFrom :
                                tableThenFrom.table[u][v] = tmpFrom
    
    print('Modified table :')
    print(tableThenTo)


def apply_oblivious_chase(list_instr, database: DataBase, iter: int):

    if 0 == len(list_instr):
        return

    for instr in list_instr:
        print('Instruction : ' + str(instr[0]))
        tableFrom = database.find_table_by_relation(instr[0].fromRel)
        tableTo = database.find_table_by_relation(instr[0].toRel)
        columnFrom = instr[0].fromAttr        
        columnTo = instr[0].toAttr

        
        allNewTuples = [] 
        count = 1 
        for i in range(1, len(tableFrom.table) + 1):
                               
            nbCol = tableTo.nb_columns

            while (count <= iter*i):
                newItem = []
                for k in range(0, nbCol):
                    if columnTo == k:                        
                        newItem.append(tableFrom.table[i][columnFrom])
        
                    else:
                        newItem.append(NoneObj(count))
                    
                allNewTuples.append(newItem)
                count += 1
    
        for tup in allNewTuples:
            tableTo.insert(tup)

        print('Modified table :')
        print(tableTo)


def apply_oblivious_skolem_chase(list_instr, database: DataBase):

    if 0 == len(list_instr):
        return

    for instr in list_instr:
        print('Instruction : ' + str(instr[0]))
        tableFrom = database.find_table_by_relation(instr[0].fromRel)
        tableTo = database.find_table_by_relation(instr[0].toRel)
        columnFrom = instr[0].fromAttr        
        columnTo = instr[0].toAttr
        allNewTuples = []
        count = 0
        for i in range(1, len(tableFrom.table) + 1):
                      
            nbCol = tableTo.nb_columns
            newItem = []
            for k in range(0, nbCol):
                count += 1
                if columnTo == k:                        
                    newItem.append(tableFrom.table[i][columnFrom])
        
                else:
                    newItem.append(NoneObj(count - i))
                
            allNewTuples.append(newItem)
            
    
        for tup in allNewTuples:
            tableTo.insert(tup)

        print('Modified table :')
        print(tableTo)
    