from infra.infrastructure import infrastructure
from infra.node import infra_node
from app.application import application
from infra import *

class first_fit_allocator:
    
    def __init__(self, infrastructure):
        self.__infrastructure = infrastructure
        
    def allocate(self, application):
        scheduled = {}
        tasks = []
        
        for key in application.get_nodes():
            scheduled[key] = False
            tasks.append(application.get_nodes()[key])
            
        return self.__recursive_alloc(tasks, scheduled, 0), scheduled
    
    def unallocate(self, task):
        n = self.__infrastructure.get_nodes()[task.scheduled_on_infra_node()]
        success = n.release_resources(task.get_n_core())
        if success:
            self.__infrastructure.get_nodes()[task.scheduled_on_infra_node()] = n
        return success
                     
    def __recursive_alloc(self, tasks, scheduled, depth):
        if depth == len(tasks):
            return True
        
        cur_task = tasks[depth]
        for n in self.__infrastructure.get_available_nodes(cur_task.get_n_core()):
            n.consume_resources(cur_task.get_n_core())
            scheduled[cur_task.get_id()] = n.get_id()
            if self.__recursive_alloc(tasks, scheduled, depth+1):
                return True
                
            n.release_resources(cur_task.get_n_core())
            
        return False