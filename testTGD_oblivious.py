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


    contr = str("P(x1,y1) -> P(x1,z)\n")
    list_instr = ch.create_instructions(contr, database)
    ch.apply_oblivious_chase(list_instr, database, 5)
    
    


if __name__ == "__main__" :
    main()
