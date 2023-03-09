from node import infra_node
from edge import infra_edge
from utils import *

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
                                human_format_to_float(n["core_frequency"]), 
                                float(n["p_static"]), 
                                float(n["k"]), 
                                float(n["alpha"]))
                
                self.__nodes[tmp.get_id()] = tmp
            except:
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
                tmp = infra_edge(str(count),
                                 e["from"],
                                 e["to"],
                                 human_format_to_float(e["resource"]))
                
                self.__edges[tmp.get_id()] = tmp
                count = count + 1
            except:
                print("Infrastructure edges are not properly formatted.")
                print("Exiting...")
                exit()
                
