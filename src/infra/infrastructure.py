from infra.node import infra_node
from infra.edge import infra_edge
from utils.utils import *
from exception.exception import InvalidConversionException

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
                tmp = infra_edge(str(count),
                                 e["from"],
                                 e["to"],
                                 human_format_to_float(e["resource"]))
                
                self.__edges[tmp.get_id()] = tmp
                count = count + 1
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
            
        print("--INFRASTRUCTURE EDGES--")
        for key in self.__edges:
            print("Edge: {} \t({}) -> ({})".format(key, self.__edges[key].get_from(), self.__edges[key].get_to()))
        print()
                
