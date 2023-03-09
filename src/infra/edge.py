class infra_edge:
    def __init__(self, id, from_node_id, to_node_id, resource):
        self.__id = id
        self.__from_node_id = from_node_id
        self.__to_node_id = to_node_id
        self.__resource = resource
        
    def get_id(self):
        return self.__id
    
    def get_from(self):
        return self.__from_node_id
    
    def get_to(self):
        return self.__to_node_id
