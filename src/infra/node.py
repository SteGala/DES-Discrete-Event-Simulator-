from utils.utils import *

class infra_node:
    
    def __init__(self, id, n_core, core_frequency_human, p_static, k, alpha):
        self.__id = id
        self.__n_cores = n_core
        self.__operating_frequency = [0 for _ in range(n_core)]
        self.__max_frequency_human = core_frequency_human
        self.__max_frequency = human_format_to_float(core_frequency_human)
        self.__p_static = p_static
        self.__k = k
        self.__alpha = alpha
        
    def get_id(self):
        return self.__id 
    
    def as_dot_label(self):
        return "Node: " + self.__id + "\nMax frequency: " + self.__max_frequency_human

    def get_max_freq_human_format(self):
        return self.__max_frequency_human
    
    def compute_power_comsumption(self):
        cons = 0
        for i in self.__operating_frequency:
            cons = cons + self.__k*(i**self.__alpha)
            
        return cons + self.__p_static
        
