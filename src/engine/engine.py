from infra.infrastructure import infrastructure
import json
import os

class engine:
    def __init__(self, conf_path):
        print("Starting simulation engine using config file {}".format(conf_path))
        
        s_conf = open(conf_path)
        simulation_conf = json.load(s_conf)
        
        self.__simulation_name = simulation_conf["name"]
        
        self.__infra = infrastructure()   
        if "infra_config" in simulation_conf:
            print("Loading infrastructure from config file {}".format(simulation_conf["infra_config"]))
            i_conf = open(simulation_conf["infra_config"])
            infrastructure_conf = json.load(i_conf)
            self.__infra.load_infrastructure(infrastructure_conf)
            i_conf.close()
        
        self.__infra.print()
        s_conf.close()