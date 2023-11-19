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
 
    
    contr1 = str("Emprunt(x1,x2) -> Livre(x2,y1,z1) and Lecteur(x1)\n")
    list_instr1 = ch.create_instructions(contr1, database)
    contr2 = str("Livre(x1,x2,x3) -> Auteur(x2,y,z)\n")
    list_instr2 = ch.create_instructions(contr2, database)
    ch.apply_TGD(list_instr1, database)
    ch.apply_TGD(list_instr2, database)
    


if __name__ == "__main__" :
    main()