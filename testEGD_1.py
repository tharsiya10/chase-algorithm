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


    contr3 = str("R(x1,x2,x5) and P(x4,x3) and x1=x3 -> Q(x3,x2,z)")
    list_instr3 = ch.create_instructions(contr3, database)
    ch.apply_EGD(list_instr3, database)


    
if __name__ == "__main__" :
    main()
