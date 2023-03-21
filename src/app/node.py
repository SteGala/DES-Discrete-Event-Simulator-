from humanize import *

class app_node:
    
    def __init__(self, id, cores, operations):
        self.__id = id
        self.__cores = cores
        self.__operations = operations
        
    def get_id(self):
        return self.__id
    
    def get_n_core(self):
        return self.__cores
    
    def get_n_operations(self):
        return self.__operations
    
    def as_dot_label(self):
        return "Node: " + self.__id + "\nN Operations: " + str(round(self.__cores, 2)) + "*" + metric(self.__operations)