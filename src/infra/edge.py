from utils.utils import *
import humanize

class infra_edge:
    
    def __init__(self, id, from_node_id, to_node_id, resource):
        self.__id = id
        self.__from_node_id = from_node_id
        self.__to_node_id = to_node_id
        self.__resource = resource
        self.__resource_used = 0
        
    def get_resource_human_format(self):
        return humanize.metric(self.__resource, precision=4, unit="b/s")
        
    def get_id(self):
        return self.__id
    
    def as_dot_label(self):
        return "Edge: " + self.__id + "\nMax bandwidth: " + humanize.metric(self.__resource, precision=4, unit="b/s")
    
    def get_from(self):
        return self.__from_node_id
    
    def get_to(self):
        return self.__to_node_id
    
    def get_percentage_available_resources(self):
        return round(self.__resource_used/self.__resource*100, 1)
    
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
