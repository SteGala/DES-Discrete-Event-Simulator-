import random
from infra.infrastructure import infrastructure
from event.event_queue import event_queue 
from utils.utils import *
import json
import os
import time
from datetime import datetime
import threading

class engine:
    def __init__(self, conf_path):
        """Instantiate the engine class. 

        Args:
            conf_path (string): path of the configuration file for the simulation.The path is relative to the root of the repository
        """        
        print("Starting simulation engine using config file {}".format(conf_path))
        
        s_conf = open(generate_os_path(conf_path))
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
            i_conf = open(generate_os_path(simulation_conf["infra_config"]))
            infrastructure_conf = json.load(i_conf)
            self.__infra.load_infrastructure(infrastructure_conf)
            i_conf.close()
        
        s_conf.close()
        
        self.__simulation_running = False
        self.__event_queue = event_queue()

        self.__simulation_running_lock = threading.Lock()
        self.__simulation_thread = threading.Thread(target=self.__main_engine_loop)
        
    def is_running(self):
        with self.__simulation_running_lock:
            return self.__simulation_running

    def start_simulation(self):
        with self.__simulation_running_lock:
            self.__simulation_running = True
        
        print("Starting simulation main thread")
        self.__simulation_thread.start()      
    
    def stop_simulation(self):
        with self.__simulation_running_lock:
            self.__simulation_running = False
            
        print("waiting for simulation main thread to join")
        self.__simulation_thread.join()
        self.__event_queue.stop()
        return
                  
    #main simulation loop, in charge of creating events to the event queue
    def __main_engine_loop(self):
        while True:
            # return if the simulation has been stopped
            with self.__simulation_running_lock:
                if not self.__simulation_running:
                    return
            
            print("ADD", flush=True)
            self.__event_queue.enqueue(myprint)
            time.sleep(random.randint(0, 10))      
        
    def dump_to_file(self):
        print("Generating report to directory {}".format(self.__out_dir))
        
        if not os.path.exists(generate_os_path(self.__out_dir)):
            print("Directory {} doesn't exist. Creating directory {}".format(self.__out_dir, self.__out_dir))
            os.mkdir(generate_os_path(self.__out_dir))
            
def myprint():
     print("Hello world")