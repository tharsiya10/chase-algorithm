
from prettytable import PrettyTable

class Type :
    def __init__(self, type) :
        self.type = type

    def __str__(self) :
        return f"{self.type}"
    
    def __eq__(self, another):
        return (self.type == another.type)

class Attribut :
    def __init__(self, nom): # param type ?
        self.nom = nom
        # self.type = type

    def __str__(self):
        return f"{self.nom}"
    
    def __eq__(self, att):
        return (self.nom == att.nom)


class Relation :
    def __init__(self, nom):
        self.nom = nom

    def __str__(self) :
        return f"{self.nom}"
    
    def __eq__(self, another):
        return (self.nom == another.nom)

class Table :
    key = 0
    table = dict()

    def __init__(self, relation, nb_columns, attr_list) :
        self.relation = relation
        self.nb_columns = nb_columns
        self.attr_list = attr_list
        self.table = {}
    
    def insert(self, list) :
        keys = self.table.keys()
        i = 1
        while i in keys :
            i += 1
        self.table[i] = list
        if i == self.key + 1:
            self.key += 1


    def __str__(self) :
        t = PrettyTable(self.attr_list)          
        for key, value in self.table.items():
            t.add_row(value)
        return '{}\n{}\n\n'.format(self.relation.nom, t)
    
    def get_index_of_attribut(self, attr):        
        try:
            index = self.attr_list.index(attr)
            print('attribute ' + str(attr) + ' has index ' + str(index) + ' in table ' + self.relation.nom)
            return index
        except Exception as e:
            print('attribute ' + str(attr) + ' is not in table ' + self.relation.nom)
            return -1


class DataBase :
    tableList = []     
    
    def __init__(self, list):
        self.tableList = list

    def __str__(self) :
        s = ""
        for table in self.tableList :
            s += table.__str__()
        return s
    
    def add_table(self, table):
        self.tableList.append(table)

    def find_table_by_relation(self, rel):
        for table in self.tableList:
            if (table.relation == rel):
                return table
        print('relation not found')
        return None
