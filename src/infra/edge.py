from utils.utils import *

class infra_edge:
    
    def __init__(self, id, from_node_id, to_node_id, resource_human_format):
        self.__id = id
        self.__from_node_id = from_node_id
        self.__to_node_id = to_node_id
        self.__resource_human_format = resource_human_format
        self.__resource = human_format_to_float(resource_human_format)
        
    def get_resource_human_format(self):
        return self.__resource_human_format
        
    def get_id(self):
        return self.__id
    
    def as_dot_label(self):
        return "Edge: " + self.__id + "\nMax bandwidth: " + self.__resource_human_format
    
    def get_from(self):
        return self.__from_node_id
    
    def get_to(self):
        return self.__to_node_id
