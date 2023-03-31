import random
from infra.infrastructure import infrastructure
from app.application import application
from event.event_queue import event_queue, event, EventType, priority
from utils.utils import *
from allocate.first_fit import first_fit_allocator
import json
import os
import csv
import datetime
from datetime import datetime as dt
import copy

class engine:
    def __init__(self, conf_path):
        """Instantiate the engine class. 
        
        Args:
            conf_path (string): path of the configuration file for the simulation.The path is relative to the root of the repository
        """        
        print("Starting simulation engine using config file {}".format(conf_path))
        
        s_conf = open(generate_os_path(conf_path))
        simulation_conf = json.load(s_conf)
        
        self.perform_preliminary_checks(simulation_conf)
        
        self.__simulation_name = simulation_conf["name"]
        
        print("Loading infrastructure from config file {}".format(simulation_conf["infra_config"]))
        self.__infra = infrastructure() 
        i_conf = open(generate_os_path(simulation_conf["infra_config"]))
        infrastructure_conf = json.load(i_conf)
        self.__infra.load_infrastructure(infrastructure_conf)
        self.__infra.save_as_dot(generate_os_path(self.__out_dir))
        i_conf.close()
            
        print("Generate placement events for the simulation")
        a_conf = open(generate_os_path(simulation_conf["app_config"]))
        application_conf = json.load(a_conf)     
        self.__generate_applications(application_conf)
        a_conf.close()
        
        self.__generate_events(simulation_conf["simulation_config"])
             
        s_conf.close()
        
        self.__allocator = self.__create_allocator(simulation_conf["simulation_config"])
        
        self.__power_events = []
        self.__resource_events = []
        self.__log_events = []
        
    def perform_preliminary_checks(self, simulation_conf):
        if "name" not in simulation_conf:
            print("Missing simulation name in config file. Filed 'name' missing")
            print("Exiting...")
            exit()
            
        if "out_dir" not in simulation_conf:
            print("Missing simulation output dir in config file. Field 'out_dir' missing")
            print("Exiting...")
            exit()
        self.__out_dir = simulation_conf["out_dir"]
        print("Generating report to directory {}".format(self.__out_dir))
        
        if not os.path.exists(generate_os_path(self.__out_dir)):
            print("Directory {} doesn't exist. Creating directory {}".format(self.__out_dir, self.__out_dir))
            os.mkdir(generate_os_path(self.__out_dir))
        else:
            print("Directory {} already exist. Please remove and execute again.")
            print("Exiting...")
            exit()
            
        if "infra_config" not in simulation_conf:
            print("Missing infrastructure template in config file. Field 'infra_config' missing")
            print("Exiting...")
            exit()
            
        if "app_config" not in simulation_conf:
            print("Missing application template in config file. Field 'app_config' missing")
            print("Exiting...")
            exit()
        
        if "simulation_config" not in simulation_conf:
            print("Missing simulation config parameters in config file. Field 'simulation_config' missing")
            print("Exiting...")
            exit()
            
    def __create_allocator(self, config):
        if "alloation_algorithm" not in config:
            print("Missing allocation algorithm parameter in config file. Field 'alloation_algorithm' missing")
            print("Exiting...")
            exit()
            
        if config["alloation_algorithm"]["name"] == "first_fit":
            return first_fit_allocator(self.__infra)
        else:
            print("Unknown allocation algorithm {}".format(config["alloation_algorithm"]["name"]))
            print("Exiting...")
            exit()
        
    def start_simulation(self):
        print("Starting simulation main loop")
        self.__main_engine_loop() 
        print("Simulation complete")     
                  
    #main simulation loop, in charge of creating events to the event queue
    def __main_engine_loop(self):
        while not self.__event_queue.is_empty():
            event = self.__event_queue.remove_next_event()
            success = self.__handle_event(event)
            self.__save_current_status(event, success)
                
        self.dump_result_to_file()
        
    def __handle_event(self, cur_event):
        if cur_event.get_event_type() == EventType.SCHEDULE:
            target_app = self.__applications[cur_event.get_app_id()]
            success, placement = self.__allocator.allocate(target_app)
            if success:
                for key in placement:
                    execution_time = self.__infra.get_nodes()[placement[key]].get_expected_completion_time(target_app.get_task_by_id(key).get_n_operations())
                    ev_date = cur_event.get_arrival_time() + datetime.timedelta(seconds=execution_time)
                    new_ev = event(target_app.get_id(), key, ev_date, self.is_event_urgent(), EventType.UNSCHEDULE)
                    self.__event_queue.add_event(new_ev)
                    target_app.get_nodes()[key].schedule_on_node(placement[key])
            else:
                if self.__retry_after_failure_seconds != 0:
                    new_ev = copy.copy(cur_event)
                    if self.__use_priority and (cur_event.get_priority() == priority.HIGH):    
                        new_ev.set_arrival_time(self.__event_queue.get_next_event_time() + datetime.timedelta(milliseconds=1))
                    else:           
                        new_ev.set_arrival_time(cur_event.get_arrival_time() + datetime.timedelta(seconds=self.__retry_after_failure_seconds))
                    self.__event_queue.add_event(new_ev)
                    
        elif cur_event.get_event_type() == EventType.UNSCHEDULE:
            target_app = self.__applications[cur_event.get_app_id()]
            success = self.__allocator.unallocate(target_app.get_nodes()[cur_event.get_task_id()])
            
        return success
                      
    def __save_current_status(self, event: event, status):
        p = {}
        r = {}
        e = {}
        p["date"] = event.get_arrival_time().strftime(time_format)
        r["date"] = event.get_arrival_time().strftime(time_format)
        e["date"] = event.get_arrival_time().strftime(time_format)
            
        for key in self.__infra.get_nodes():
            p[key] = self.__infra.get_nodes()[key].compute_power_comsumption()
            r[key] = self.__infra.get_nodes()[key].compute_resource_usage()
            
        self.__power_events.append(p)
        self.__resource_events.append(r)
        
        e["type"] = event.get_event_type().name
        e["success"] = status
        
        if event.get_event_type() == EventType.SCHEDULE:
            e["note"] = "App: {}".format(event.get_app_id())
        else:
            e["note"] = "Task: {}".format(event.get_task_id())
        
        self.__log_events.append(e)
        
    def __generate_events(self, config):
        if ("start_date" not in config) or ("end_date" not in config) or ("event_distribution" not in config) or ("application_urgency_ratio" not in config):
            print("Simulation config is not properly defined, missing one or more of the fields 'start_date', 'end_date', 'event_distribution', 'application_urgency_ratio'")
            print("Exiting...")
            exit()
        
        accepted_distribution = ["random"]
        if config["event_distribution"] not in accepted_distribution:
            print("Event distribution '{}' not supported. Select one {}".format(config["event_distribution"], accepted_distribution))
            print("Exiting...")
            exit()
            
        self.__application_urgency = float(config["application_urgency_ratio"])
        self.__start_date = dt.strptime(config["start_date"], time_format)
        self.__end_date = dt.strptime(config["end_date"], time_format)
        
        if "scheduling_algorithm" not in config:
            print("Simulation config is not properly defined, missing 'scheduling_algorithm' configuration.")
            print("Exiting...")
            exit()
            
        self.__event_queue = event_queue(config["scheduling_algorithm"]["name"])
        
        if ("retry_after_failure_seconds" not in config["scheduling_algorithm"]) or ("use_priority" not in config["scheduling_algorithm"]):
            print("Simulation config is not properly defined, missing 'retry_after_failure_seconds' or 'use_priority' configuration.")
            print("Exiting...")
            exit()
            
        self.__retry_after_failure_seconds = int(config["scheduling_algorithm"]["retry_after_failure_seconds"])
        self.__use_priority = config["scheduling_algorithm"]["use_priority"]
        
        count = 0
        for app in self.__applications:
            rand_date = random_date(self.__start_date, self.__end_date, random.random())
            is_urgent = self.is_event_urgent()
            
            e = event(self.__applications[app].get_id(), list(self.__applications[app].get_nodes().keys()), rand_date, is_urgent, EventType.SCHEDULE)
            self.__event_queue.add_event(e)
            count = count + 1
    
    def __generate_applications(self, app_conf):
        self.__applications = {}
        
        if not check_correct_application_config(app_conf):
            print("The application config file is not correct.")
            print("Exiting...")
            exit()
            
        for i in range(int(app_conf["number_of_applications"])):
            a = application(generate_app_name(i), app_conf["app_spec"])
            self.__applications[generate_app_name(i)] = a
            a.save_as_dot(generate_os_path(self.__out_dir))
            
    def is_event_urgent(self):
        r = random.random()
        if r <= self.__application_urgency:
            return priority.HIGH
        return priority.LOW   
        
    def dump_events_to_file(self):          
        with open(os.path.join(generate_os_path(self.__out_dir), "events.csv"), 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.__event_queue.field_names())
            writer.writeheader()
            writer.writerows(self.__event_queue.format_csv())
            pass
    def dump_result_to_file(self):
        print("Generating output result files")
        node_names = self.__infra.get_nodes_name()
        node_headers = ["date"]
        node_headers.extend(node_names)
        log_headers = ["date", "type", "success", "note"]
        
        with open(os.path.join(generate_os_path(self.__out_dir), "power_events.csv"), 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=node_headers)
            writer.writeheader()
            writer.writerows(self.__power_events)
            
        with open(os.path.join(generate_os_path(self.__out_dir), "resource_events.csv"), 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=node_headers)
            writer.writeheader()
            writer.writerows(self.__resource_events)
            
        with open(os.path.join(generate_os_path(self.__out_dir), "log_events.csv"), 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=log_headers)
            writer.writeheader()
            writer.writerows(self.__log_events)
        
            
            
        
        
            
