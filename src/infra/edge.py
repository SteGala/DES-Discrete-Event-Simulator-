from utils.utils import *

class infra_edge:
    
    def __init__(self, id, from_node_id, to_node_id, resource_human_format):
        self.__id = id
        self.__from_node_id = from_node_id
        self.__to_node_id = to_node_id
        self.__resource_human_format = resource_human_format
        self.__resource = human_format_to_float(resource_human_format)
        self.__resource_used = 0
        
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
    
    def can_host(self, amount):
        if self.__resource_used + amount > self.__resource:
            return False
        return True
    
    def consume_resources(self, amount):
        if not self.can_host(amount):
            return False
        
        self.__resource_used = self.__resource_used + amount
        return True
    
    def release_resources(self, amount):
        if self.__resource_used < amount:
            return False
        
        self.__resource_used = self.__resource_used - amount
        return True
