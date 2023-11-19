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


    contr3 = str("R(x1,y1,z1) and Q(y2,x2,z2) and y1=y2 -> x1=x2\n")
    list_instr3 = ch.create_instructions(contr3, database)
    ch.apply_EGD(list_instr3, database)
    
    


if __name__ == "__main__" :
    main()

