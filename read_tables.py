import csv
from database import *

def read_table(filename, table_name) :
    try :
        with open(filename, 'r') as file:
            csvreader = csv.reader(file, delimiter=',')
            attributs = next(csvreader)
            attrList = []
            for a in attributs :
                attrList.append(Attribut(a))
            relation = Relation(table_name)
            table = Table(relation, len(attrList), attrList)
            # TODO check for NULL and empty values 
            for row in csvreader :
                table.insert(row)
            return table
                
            
    except :
        print("Could not read file")


