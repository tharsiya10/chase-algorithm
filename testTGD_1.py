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
    
  
    contr1 = str("R(x1,x2,x3) -> Q(x2,x1,z1) and P(x1,r)\n")  # 3 instr to apply
    list_instr1 = ch.create_instructions(contr1, database)  
    ch.apply_TGD(list_instr1, database)


if __name__ == "__main__" :
    main()
