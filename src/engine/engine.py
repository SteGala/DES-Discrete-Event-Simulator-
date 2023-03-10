from infra.infrastructure import infrastructure
import json
import os

class engine:
    def __init__(self, conf_path):
        """Instantiate the engine class. 

        Args:
            conf_path (string): path of the configuration file for the simulation.The path is relative to the root of the repository
        """        
        conf_path_rel = os.path.join("..", conf_path) 
        print("Starting simulation engine using config file {}".format(conf_path))
        
        s_conf = open(conf_path_rel)
        simulation_conf = json.load(s_conf)
        
        if "name" not in simulation_conf:
            print("Missing simulation name in config file. Filed 'name' missing")
            print("Exiting...")
            exit()
        self.__simulation_name = simulation_conf["name"]
        
        if "out_dir" not in simulation_conf:
            print("Missing simulation output dir in config file. Field 'out_dir' missing")
            print("Exiting...")
            exit()
        self.__out_dir = simulation_conf["out_dir"]
        
        self.__infra = infrastructure()   
        if "infra_config" in simulation_conf:
            print("Loading infrastructure from config file {}".format(simulation_conf["infra_config"]))
            infra_path = os.path.join("..", simulation_conf["infra_config"])
            i_conf = open(infra_path)
            infrastructure_conf = json.load(i_conf)
            self.__infra.load_infrastructure(infrastructure_conf)
            i_conf.close()
        
        self.__infra.print()
        s_conf.close()
        
    def dump_to_file(self):
        print("Generating report to {}".format(self.__out_dir))