from humanize import *

class app_edge:
    
    def __init__(self, id, from_node_id, to_node_id, resources):
        self.__id = id
        self.__from_node_id = from_node_id
        self.__to_node_id = to_node_id
        self.__resources = resources
        
    def get_from(self):
        return self.__from_node_id
    
    def get_to(self):
        return self.__to_node_id
    
    def as_dot_label(self):
        return "Edge: " + self.__id + "\nMax bandwidth: " + metric(self.__resources)