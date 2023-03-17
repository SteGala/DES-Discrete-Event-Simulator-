from infra.node import infra_node
from infra.edge import infra_edge
from utils.utils import *
from exception.exception import InvalidConversionException
import pygraphviz as pgv

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
            
        for n in infra_json["nodes"]:
            try:
                tmp = infra_node(n["id"], 
                                int(n["n_core"]),  
                                n["core_frequency"],
                                float(n["p_static"]), 
                                float(n["k"]), 
                                float(n["alpha"]))
                
                self.__nodes[tmp.get_id()] = tmp
                self.__edges[tmp.get_id()] = []
            except InvalidConversionException:
                print("Error converting node {} core_frequency.".format(n["id"]))
                print("Exiting...")
                exit()
            except Exception as e:
                print("Infrastructure nodes are not properly formatted.")
                print("Exiting...")
                exit()
                
        if "edges" not in infra_json:
            print("Missing infrastructure edges.")
            print("Exiting...")
            exit()
                
        count = 0
        for e in infra_json["edges"]:
            try:
                tmp1 = infra_edge(generate_infra_edge_id(count),
                                 e["from"],
                                 e["to"],
                                 e["resource"])
                tmp2 = infra_edge(generate_infra_edge_id(count+1),
                                 e["to"],
                                 e["from"],
                                 e["resource"])
                
                self.__edges[e["from"]].append(tmp1)
                self.__edges[e["to"]].append(tmp2)
                count = count + 2
            except InvalidConversionException:
                print("Error converting edge {} core_frequency.".format(count))
                print("Exiting...")
                exit()
            except:
                print("Infrastructure edges are not properly formatted.")
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
                
        G.write(os.path.join(path, "infrastructure.dot"))
        
        
        
                
