from humanize import *

class app_node: 
    def __init__(self, id, cores, operations):
        self.__id = id
        self.__cores = cores
        self.__operations = operations
        self.__scheduled_on = ""
        
    def get_id(self):
        return self.__id
    
    def get_n_core(self):
        return self.__cores
    
    def get_n_operations(self):
        return self.__operations
    
    def scheduled_on_infra_node(self):
        return self.__scheduled_on
    
    def schedule_on_node(self, node_id):
        self.__scheduled_on = node_id
    
    def as_dot_label(self):
        return "Node: " + self.__id + "\nN Operations: " + str(round(self.__cores, 2)) + "*" + metric(self.__operations)