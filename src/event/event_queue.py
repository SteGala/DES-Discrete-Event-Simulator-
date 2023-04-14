from utils.utils import *
from enum import Enum
from app.application import application_class

class EventType(Enum):
    SCHEDULE = 1
    UNSCHEDULE = 2

class priority(Enum):
    LOW = 0
    HIGH = 1
    
class event_behavior(Enum):
    FIFO = 0

class event:
    def __init__(self, app, task_ids, arrival_time, event_time, priority, type):
        self.__app = app
        self.__task_ids = task_ids
        self.__event_time = event_time
        self.__priority = priority
        self.__event_type = type
        self.__retry = 0
        self.__arrival_time = arrival_time
        
    def to_dict(self):
        return {"id": self.__event_id,
                "app_id": self.__app.get_id(),
                "task_id": self.__task_ids,
                "arrival_time": self.__event_time.strftime(time_format),
                "priority": self.__priority}       
    
    def get_event_time(self):
        return self.__event_time 
    
    def get_elapsed_time_in_seconds(self):
        return (self.__event_time - self.__arrival_time).total_seconds()
    
    def increase_retry(self):
        self.__retry = self.__retry + 1
        
    def get_retry_number(self):
        return self.__retry
    
    def set_event_time(self, event_time):
        self.__event_time = event_time
        
    def get_arrival_time(self):
        return self.__arrival_time
    
    def set_event_id(self, event_id):
        self.__event_id = event_id
        
    def get_app_id(self):
        return self.__app.get_id()
    
    def get_application(self):
        return self.__app
    
    def get_event_type(self):
        return self.__event_type
    
    def get_task_id(self):
        return self.__task_ids
    
    def get_priority(self):
        return self.__priority
    

class event_queue:
    def __init__(self, behaviour):
        self.events = {}
        self.__event_id = 0
        
        for a_class in application_class:
            self.events[a_class.value] = []
        
        accepted_behaviour = [e.name for e in event_behavior]
        if behaviour["name"] not in accepted_behaviour:
            print("Unrecognised scheduling behaviour {}. Accepted values are: {}".format(behaviour["name"], accepted_behaviour))
            print("Exiting...")
            exit()
            
        self.__behaviour = event_behavior[behaviour["name"]]
        self.__label = behaviour["label"]
        
        if self.__behaviour == event_behavior.FIFO:
            if ("retry_after_failure_seconds" not in behaviour) or ("use_priority" not in behaviour):
                print("Simulation config is not properly defined, missing 'retry_after_failure_seconds' or 'use_priority' configuration.")
                print("Exiting...")
                exit()
                
            self.__retry_after_failure_seconds = int(behaviour["retry_after_failure_seconds"])
            self.__use_priority = behaviour["use_priority"]
            
    def get_label(self):
        return self.__label
    
    def get_retry_time(self):
        return self.__retry_after_failure_seconds
    
    def use_priority(self):
        return self.__use_priority
        
    def add_event(self, event):
        if self.__behaviour == event_behavior.FIFO:
            self.__add_fifo(event)
            
    def remove_next_event(self):
        if self.__behaviour == event_behavior.FIFO:
            return self.__remove_fifo()
                 
    def __add_fifo(self, event: event):
        event.set_event_id(generate_event_id(self.__event_id))
        self.__event_id = self.__event_id + 1
        
        app_class = event.get_application().get_application_class().value
        
        if not self.events[app_class]:
            self.events[app_class].append(event)
        else:
            for i, e in enumerate(self.events[app_class]):
                if event.get_event_time() < e.get_event_time():
                    self.events[app_class].insert(i, event)
                    break
            else:
                self.events[app_class].append(event)
                
    def __remove_fifo(self):
        target_list = ""
        most_recent_event_date = ""
        
        for key in self.events:
            if self.events[key]:
                if most_recent_event_date == "" or self.events[key][0].get_event_time() < most_recent_event_date:
                    target_list = key
                    most_recent_event_date = self.events[key][0].get_event_time()
            
        if target_list != "":
            return self.events[target_list].pop(0)
        
        return None
        
    def get_next_event_time(self):
        target_list = ""
        most_recent_event_date = ""
        
        for key in self.events:
            if self.events[key]:
                if most_recent_event_date == "" or self.events[key][0].get_event_time() < most_recent_event_date:
                    target_list = key
                    most_recent_event_date = self.events[key][0].get_event_time()
            
        if target_list != "":
            return most_recent_event_date
        return None
    
    def get_next_unschedule_event_time(self):  
        target_list = ""
        most_recent_event_date = ""
              
        for key_ev in self.events:
            for ev in self.events[key_ev]:
                if ev.get_event_type() == EventType.UNSCHEDULE and (most_recent_event_date == "" or ev.get_event_time() < most_recent_event_date):
                    target_list = key_ev
                    most_recent_event_date = ev.get_event_time()
        
        if target_list != "":
            return most_recent_event_date
        return None
        
    def is_empty(self):
        for key in self.events:
            if len(self.events[key]) != 0:
                return False
        return True
    
    def format_csv(self):
        ret = []
        for e in self.events:
            ret.append(e.to_dict())
        return ret
    
    def field_names(self):
        return ["id", "app_id", "task_id", "arrival_time", "priority"]
