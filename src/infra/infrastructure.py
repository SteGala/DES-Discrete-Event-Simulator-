import heapq
from infra.node import infra_compute_node, infra_network_node
from infra.edge import infra_edge
from utils.utils import *
from exception.exception import InvalidConversionException
import pygraphviz as pgv
import random

random.seed(10)

class infrastructure:

    def __init__(self):
        self.__nodes = {}
        self.__edges = {}
        self.__name = ""
        
    def get_name(self):
        return self.__name

    def load_infrastructure(self, infra_json):
        self.__name = infra_json["name"]
        
        if "nodes" not in infra_json:
            print("Missing infrastructure nodes.")
            print("Exiting...")
            exit()
            
        count_nodes = 0
        count_net_nodes = 0
        count_edges = 0
        net_nodes = []
        
        for n in infra_json["nodes"]:
            net = infra_network_node(generate_infra_network_node_id(count_net_nodes))
            count_net_nodes = count_net_nodes + 1
            self.__nodes[net.get_id()] = net
            self.__edges[net.get_id()] = []
            net_nodes.append(net)
            
            try:
                for _ in range(int(n["replicas"])):
                    n_core = random.randint(int(n["n_core_min"]), int(n["n_core_max"]))
                    core_frequency = random.uniform(human_format_to_float(n["core_frequency_min"]), human_format_to_float(n["core_frequency_max"]))
                    p_static = random.uniform(float(n["p_static_min"]), float(n["p_static_max"]))
                    k = random.uniform(float(n["k_min"]), float(n["k_max"]))
                    alpha = random.uniform(float(n["alpha_min"]), float(n["alpha_max"]))
                    
                    tmp = infra_compute_node(generate_infra_node_id(count_nodes), 
                                    n_core,  
                                    core_frequency,
                                    p_static, 
                                    k, 
                                    alpha)
                    
                    self.__nodes[tmp.get_id()] = tmp
                    self.__edges[tmp.get_id()] = []
                    
                    resource = random.uniform(human_format_to_float(n["network"]["min_resource"]), human_format_to_float(n["network"]["max_resource"]))
                    
                    tmp1 = infra_edge(generate_infra_edge_id(count_edges),
                                 net.get_id(),
                                 tmp.get_id(),
                                 resource)
                    tmp2 = infra_edge(generate_infra_edge_id(count_edges+1),
                                    tmp.get_id(),
                                    net.get_id(),
                                    resource)
                    
                    self.__edges[net.get_id()].append(tmp1)
                    self.__edges[tmp.get_id()].append(tmp2)
                    
                    count_nodes = count_nodes + 1
                    count_edges = count_edges + 2
            except InvalidConversionException:
                print("Error converting node {} core_frequency.".format(n["id"]))
                print("Exiting...")
                exit()
            except Exception as e:
                print(e)
                print("Infrastructure nodes are not properly formatted.")
                print("Exiting...")
                exit()
        
        try:
            res = human_format_to_float(infra_json["network"])
            for i in range(len(net_nodes)-1):
                for j in range(i+1, len(net_nodes)):
                    e1 = infra_edge(generate_infra_edge_id(count_edges),
                                    net_nodes[i].get_id(),
                                    net_nodes[j].get_id(),
                                    res)
                    e2 = infra_edge(generate_infra_edge_id(count_edges + 1),
                                    net_nodes[j].get_id(),
                                    net_nodes[i].get_id(),
                                    res)
                    
                    self.__edges[net_nodes[i].get_id()].append(e1)
                    self.__edges[net_nodes[j].get_id()].append(e2)
                    
                    count_edges = count_edges + 1
        except Exception as e:
                print(e)
                print("Infrastructure network is not properly formatted.")
                print("Exiting...")
                exit()
    def print(self):
        print()
        print("--INFRASTRUCTURE NODES--")
        for key in self.__nodes:
            print("Node: {}".format(self.__nodes[key].get_id()))
            
        print()
        print("--INFRASTRUCTURE EDGES--")
        for key in self.__edges:
            print("Node: {}".format(key), end="")
            for e in self.__edges[key]:
                print("\t(X) -> ({})".format(e.get_to()), end="")
            print()
        print()
        
    def get_available_nodes(self, n_core):
        ret = []
        
        for key in self.__nodes:
            if isinstance(self.__nodes[key], infra_compute_node) and self.__nodes[key].can_host(n_core):
                ret.append(self.__nodes[key])
                
        return ret
    
    def get_nodes(self):
        return self.__nodes
    
    def get_nodes_name(self):
        return list(self.__nodes.keys())
        
    def save_as_dot(self, path):
        G = pgv.AGraph(directed=True)
        G.node_attr["shape"] = "box"
        G.graph_attr["label"] = self.__summarize_infrastructure()
        
        for key in self.__edges:
            for e in self.__edges[key]:
                G.add_edge(e.get_from(), e.get_to(), label=e.as_dot_label())
                n = G.get_node(e.get_from())  
                n.attr["label"] = self.__nodes[e.get_from()].as_dot_label()
                n = G.get_node(e.get_to())  
                n.attr["label"] = self.__nodes[e.get_to()].as_dot_label()      
                
        G.write(os.path.join(path, "infrastructure.dot"))
        
    def get_node_edges(self, node_id):
        return self.__edges[node_id]
    
    def consume_edge_resources(self, from_id, to_id, amount):
        edges = self.__find_path_between_nodes(from_id, to_id)
        
        for e in edges:
            if not e.can_host(amount):
                return False
            
        for e in edges:
            e.consume_resources(amount)
            
        return True
        
    
    def release_edge_resources(self, from_id, to_id, amount):
        edges = self.__find_path_between_nodes(from_id, to_id)
            
        for e in edges:
            e.release_resources(amount)
            
    def summarize_edges(self):
        result = {}
        
        for key in self.__edges:
            for e in self.__edges[key]:
                result[e.get_id()] = e.get_percentage_available_resources()
                
        return result
        
    def __summarize_infrastructure(self):
        count = 0
        for key in self.__edges:
            for i in self.__edges[key]:
                count = count + 1
        return "{} \nNumber of nodes: {} \nNumber of edges: {}".format(self.__name, len(self.__nodes), count)
    
    def __find_path_between_nodes(self, n1, n2):
        #print("From {} to {}".format(n1, n2))
        edges = []
        id1 = ""
        id2 = ""
        
        # n1 --> network node
        for e in self.__edges[n1]:
            if isinstance(self.__nodes[e.get_to()], infra_network_node):
                edges.append(e)
                id1 = e.get_to()
                for e1 in self.__edges[id1]:
                    if e1.get_to() == n1:
                        edges.append(e1)
                        break
                break
            
        # n2 --> network node
        for e in self.__edges[n2]:
            if isinstance(self.__nodes[e.get_to()], infra_network_node):
                edges.append(e)
                id2 = e.get_to()
                for e1 in self.__edges[id2]:
                    if e1.get_to() == n2:
                        edges.append(e1)
                        break
                break
          
        # network node --> network node  
        for e in self.__edges[id1]:
            if e.get_to() == id2:
                edges.append(e)
                for e1 in self.__edges[id2]:
                    if e1.get_to() == id1:
                        edges.append(e1)
                        break
                break
            
        return edges
        
        
        
                
