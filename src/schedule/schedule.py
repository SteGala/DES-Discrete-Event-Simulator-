from infra.infrastructure import infrastructure
from infra.node import infra_node
from app.application import application
from infra import *

class dummy_scheduler:
    
    def __init__(self, infrastructure):
        self.__infrastructure = infrastructure
        
    def schedule(self, application):
        scheduled = {}
        tasks = []
        
        for key in application.get_nodes():
            scheduled[key] = False
            tasks.append(application.get_nodes()[key])
            
        return self.__recursive_schedule(tasks, scheduled, 0), scheduled
                     
    def __recursive_schedule(self, tasks, scheduled, depth):
        if depth == len(tasks):
            print(scheduled)
            return True
        
        cur_task = tasks[depth]
        for n in self.__infrastructure.get_available_nodes(cur_task.get_n_core(), cur_task.get_n_operations()):
            n.consume_resources(cur_task.get_n_core(), cur_task.get_n_operations())
            scheduled[cur_task.get_id()] = n.get_id()
            if self.__recursive_schedule(tasks, scheduled, depth+1):
                return True
                
            n.release_resources(cur_task.get_n_core(), cur_task.get_n_operations())
            
        return False