import random
from app.node import app_node
from app.edge import app_edge
from utils.utils import *
import pygraphviz as pgv
from enum import Enum

random.seed(10)

class application_class(Enum):
    DB = 1
    HPC = 2
    WEB = 3

class application:
    
    def __init__(self, id, config):
        self.__id = id
        
        self.__create_randomized_application(config)
        
    def get_id(self):
        return self.__id
    
    def get_nodes(self):
        return self.__nodes
    
    def get_node(self, id):
        return self.__nodes[id]
        
    def __create_randomized_application(self, config):
        self.__nodes = {}
        self.__edges = {}
        self.__class = random.choice(list(application_class))
        
        min_n_node = int(config["min_n_node"])
        max_n_node = int(config["max_n_node"])
        n_node = random.randint(min_n_node, max_n_node)
        
        min_task_n_core_requirements = human_format_to_float(config["min_task_n_core_requirements"])
        max_task_n_core_requirements = human_format_to_float(config["max_task_n_core_requirements"])
        
        min_task_operation_requirements = human_format_to_float(config["min_task_operation_requirements"])
        max_task_operation_requirements = human_format_to_float(config["max_task_operation_requirements"])
        
        for i in range(n_node):
            task_n_core_requirements = random.uniform(min_task_n_core_requirements, max_task_n_core_requirements)
            task_operation_requirements = random.uniform(min_task_operation_requirements, max_task_operation_requirements)
            
            n = app_node(generate_app_node_id(self.__id, i), task_n_core_requirements, task_operation_requirements)
            self.__nodes[generate_app_node_id(self.__id, i)] = n
            self.__edges[generate_app_node_id(self.__id, i)] = []
            
        task_connectivity_ratio = float(config["task_connectivity_ratio"])
        n_edge = (n_node * (n_node - 1))/2
        n_edge = int(n_edge*task_connectivity_ratio)
        self.__n_edges = 0
        
        min_task_edge_requirements = human_format_to_float(config["min_task_edge_requirements"])
        max_task_edge_requirements = human_format_to_float(config["max_task_edge_requirements"])
        
        while self.__n_edges < n_edge:
            n1 = random.randint(0, n_node-1)
            n2 = random.randint(0, n_node-1)
            
            if n1 != n2 and not self.__has_edge(n1, n2):
                task_edge_requirements = random.uniform(min_task_edge_requirements, max_task_edge_requirements)
                e1 = app_edge(generate_app_edge_id(self.__n_edges), generate_app_node_id(self.__id, n1), generate_app_node_id(self.__id, n2), task_edge_requirements)
                e2 = app_edge(generate_app_edge_id(self.__n_edges), generate_app_node_id(self.__id, n2), generate_app_node_id(self.__id, n1), task_edge_requirements)
                
                self.__edges[generate_app_node_id(self.__id, n1)].append(e1)
                self.__edges[generate_app_node_id(self.__id, n2)].append(e2)
                
                self.__n_edges = self.__n_edges + 1
       
    def get_application_class(self):
        return self.__class
    
    def reset(self):
        for n in self.__nodes:
            self.__nodes[n].reset()
            
    def __has_edge(self, node1, node2):
        for e in self.__edges[generate_app_node_id(self.__id, node1)]:
            if e.get_to() == generate_app_node_id(self.__id, node2):
                return True
        return False
    
    def get_task_by_id(self, task_id):
        return self.__nodes[task_id]
    
    def get_task_n_operations(self, task_id):
        return self.__nodes[task_id].get_n_operations()
                    
    def connectedComponents(self):
        visited = []
        cc = []
        for i in range(self.__nodes):
            visited.append(False)
        for v in range(self.__nodes):
            if visited[v] == False:
                temp = []
                cc.append(self.DFSUtil(temp, v, visited))
        return cc
    
    def DFSUtil(self, temp, v, visited):
 
        # Mark the current vertex as visited
        visited[v] = True
 
        # Store the vertex to list
        temp.append(v)
 
        # Repeat for all vertices adjacent
        # to this vertex v
        for i in self.adj[v]:
            if visited[i] == False:
 
                # Update the list
                temp = self.DFSUtil(temp, i, visited)
        return temp
    
    def print(self):
        print()
        print("--APPLICATION NODES--")
        for key in self.__nodes:
            print("Node: {}".format(self.__nodes[key].get_id()))
        
        print()
        print("--APPLICATION EDGES--")
        for key in self.__edges:
            print("Node: {}".format(key), end=" ")
            for e in self.__edges[key]:
                print("\t(X) -> ({})".format(e.get_to()), end="")
            print()
        print()
        
    def get_node_edges(self, node_id):
        return self.__edges[node_id]
        
    def save_as_dot(self, path):
        G = pgv.AGraph(directed=False)
        G.node_attr["shape"] = "box"
        
        for key in self.__edges:
            for e in self.__edges[key]:
                G.add_edge(e.get_from(), e.get_to(), label=e.as_dot_label())
                n = G.get_node(e.get_from())  
                n.attr["label"] = self.__nodes[e.get_from()].as_dot_label()
                n = G.get_node(e.get_to())  
                n.attr["label"] = self.__nodes[e.get_to()].as_dot_label()      
                
        G.write(os.path.join(path, "application_" + self.__id + ".dot"))