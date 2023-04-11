from infra.infrastructure import infrastructure
from infra.node import infra_compute_node
from app.application import application
from infra import *

class first_fit_allocator:
    
    def __init__(self, infrastructure: infrastructure):
        self.__infrastructure = infrastructure
        
    def allocate(self, application: application):
        scheduled = {}
        tasks = []
        
        for key in application.get_nodes():
            scheduled[key] = False
            tasks.append(application.get_nodes()[key])
            
        return self.__recursive_alloc(tasks, scheduled, application, 0), scheduled
    
    def unallocate(self, task_id, application):
        task = application.get_node(task_id)
        task.unallocate()
        
        # release node resources
        n = self.__infrastructure.get_nodes()[task.scheduled_on_infra_node()]
        success = n.release_resources(task.get_n_core())
        
        if success:
            self.__infrastructure.get_nodes()[task.scheduled_on_infra_node()] = n
        else:
            # shoulf never happen
            return False
            
        # release edge resources
        edges = application.get_node_edges(task.get_id())
       
        # bisogna resettare questi flag
        for e in edges:
            if task.scheduled_on_infra_node() != application.get_node(e.get_to()).scheduled_on_infra_node() and not application.get_node(e.get_to()).is_unallocated():
                self.__infrastructure.release_edge_resources(task.scheduled_on_infra_node(), application.get_node(e.get_to()).scheduled_on_infra_node(), e.get_amount())
                
        return True
                        
    def __recursive_alloc(self, tasks, scheduled, application:application, depth):
        if depth == len(tasks):
            return True
        
        cur_task = tasks[depth]
        for n in self.__infrastructure.get_available_nodes(cur_task.get_n_core()):
            n.consume_resources(cur_task.get_n_core())
            scheduled[cur_task.get_id()] = n.get_id()
            
            tmp = {}
            fail = False
            for e in application.get_node_edges(cur_task.get_id()):
                # funziona ma è orribile
                if scheduled[e.get_to()] and scheduled[e.get_to()] != n.get_id():
                    if self.__infrastructure.consume_edge_resources(scheduled[e.get_to()], n.get_id(), e.get_amount()):
                        tmp[scheduled[e.get_to()]] = n.get_id()
                    else:
                        #tmp[scheduled[e.get_to()]] = n.get_id()
                        scheduled[cur_task.get_id()] = False
                        fail = True
                        break
            
            if fail:
                for key in tmp:
                    print(cur_task.get_id())
                    self.__infrastructure.release_edge_resources(key, tmp[key], e.get_amount())
                
                n.release_resources(cur_task.get_n_core())
                continue
            
            if self.__recursive_alloc(tasks, scheduled, application, depth+1):
                return True
                
            for e in application.get_node_edges(cur_task.get_id()):
                # funziona ma è orribile
                if scheduled[e.get_to()] and scheduled[e.get_to()] != n.get_id():
                    self.__infrastructure.release_edge_resources(scheduled[e.get_to()], n.get_id(), e.get_amount())

            n.release_resources(cur_task.get_n_core())
        
        scheduled[cur_task.get_id()] = False    
        return False