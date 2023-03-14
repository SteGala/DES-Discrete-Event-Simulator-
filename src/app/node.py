class app_node:
    
    def __init__(self, id, cores, operations):
        self.__id = id
        self.__cores = cores
        self.__operations = operations
        
    def get_id(self):
        return self.__id