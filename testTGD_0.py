from read_tables import *
from contraintes import *
import chase_parser as chp
import chase as ch

def main() :
    list = []

    tableR = read_table('csv/R.csv', 'R')
    tableP = read_table('csv/P.csv', 'P')
    tableQ = read_table('csv/Q.csv', 'Q')
    
    list.append(tableR)
    list.append(tableP)
    list.append(tableQ)
    
    print('Initial Data Base :')
    database = DataBase(list)
    print(database)
    
  
    contr1 = str("R(x0,x1,x2) -> Q(x2,z1,z2) and P(x0,z3)\n")
    list_instr1 = ch.create_instructions(contr1, database)  
    ch.apply_TGD(list_instr1, database)


if __name__ == "__main__" :
    main()
