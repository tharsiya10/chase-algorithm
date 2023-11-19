from read_tables import *
from contraintes import *
import chase_parser as chp
import chase as ch

def main() :
    list = []

    livre = read_table('csv/Livre.csv' , 'Livre')
    auteur = read_table('csv/Auteur.csv' , 'Auteur')
    emprunt = read_table('csv/Emprunt.csv' , 'Emprunt')
    lecteur = read_table('csv/Lecteur.csv' , 'Lecteur')
 
 
 
    list.append(livre)
    list.append(auteur)
    list.append(emprunt)
    list.append(lecteur)
    
    database = DataBase(list)
    print(database)

    tableR = read_table('csv/R.csv', 'R')
    tableP = read_table('csv/P.csv', 'P')
    tableQ = read_table('csv/Q.csv', 'Q')
    
    list.append(tableR)
    list.append(tableP)
    list.append(tableQ)
    
    database = DataBase(list)
    print(database)
    
  
    contr1 = str("R(x1,x2,x3) -> Q(x2,x1,z1) and P(x1,r)\n")  # 3 instr to apply
    list_instr1 = ch.create_instructions(contr1, database)  
    ch.apply_TGD(list_instr1, database)

    contr3 = str("Q(x1,y1,z1) and P(y2,x2) and y1=y2 -> x1=x2\n")
    list_instr3 = ch.create_instructions(contr3, database)
    ch.apply_EGD(list_instr3, database)
    


    contr4 = str("R(x1,y1,z1) and P(y2,x2,z2) and y1=y2 -> x1=x2\n")
    list_instr4 = ch.create_instructions(contr4, database)
    ch.apply_EGD(list_instr4, database)
    

    contr5 = str("R(x1,x2,x5) and P(x4,x3) and x1=x3 -> Q(x3,x2)")
    list_instr5 = ch.create_instructions(contr5, database)
    print(list_instr5)

    


if __name__ == "__main__" :
    main()

