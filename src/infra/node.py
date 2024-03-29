from utils.utils import *
from enum import Enum
import humanize

class infra_compute_node:
    
    def __init__(self, id, n_core, core_frequency, p_static, k, alpha):
        self.__id = id
        self.__n_cores = n_core
        self.__n_cores_used = 0
        self.__operating_frequency = [0 for _ in range(n_core)]
        self.__max_frequency = core_frequency
        self.__p_static = p_static
        self.__k = k
        self.__alpha = alpha
        
    def get_id(self):
        return self.__id 
    
    def as_dot_label(self):
        return "Node: " + self.__id + "\nMax frequency: " + humanize.metric(self.__max_frequency, precision=4, unit="hz")

    def get_max_freq_human_format(self):
        return  humanize.metric(self.__max_frequency, precision=4, unit="hz")
    
    def compute_power_comsumption(self):
        cons = 0
        for i in self.__operating_frequency:
            cons = cons + self.__k*(i**self.__alpha)
            
        return cons + self.__p_static
    
    def compute_resource_usage(self):
        return round((self.__operating_frequency[0] / self.__max_frequency) * 100, 2)
    
    def can_host(self, n_core):
        if self.__n_cores_used + n_core > self.__n_cores:
            return False
        return True
    
    def consume_resources(self, n_core):
        if not self.can_host(n_core):
            return False
        
        tot = n_core * self.__max_frequency
        load_per_core = tot / self.__n_cores
        
        for i in range(len(self.__operating_frequency)):
            self.__operating_frequency[i] = self.__operating_frequency[i] + int(load_per_core)
            
        self.__n_cores_used = self.__n_cores_used + n_core
        return True
    
    def release_resources(self, n_core):
        tot = n_core * self.__max_frequency
        load_per_core = int(tot / self.__n_cores)
        
        for i in range(len(self.__operating_frequency)):
            if self.__operating_frequency[i] < load_per_core:
                return False
            self.__operating_frequency[i] = self.__operating_frequency[i] - load_per_core

        self.__n_cores_used = self.__n_cores_used - n_core
        return True
    
    def get_expected_completion_time(self, operations):
        return operations/self.__max_frequency
        
        
class infra_network_node:
    
    def __init__(self, id):
        self.__id = id
        
    def get_id(self):
        return self.__id
    
    def as_dot_label(self):
        return self.__id
    
    def compute_resource_usage(self):
        return 0
    
    def compute_power_comsumption(self):
        return 0
