from utils.utils import *

class EventType(enumerate):
    SCHEDULE = 1
    UNSCHEDULE = 2

class priority(enumerate):
    LOW = 0
    HIGH = 1

class event:
    def __init__(self, app_id, task_ids, arrival_time, priority, type):
        self.__app_id = app_id
        self.__task_ids = task_ids
        self.__arrival_time = arrival_time
        self.__priority = priority
        self.__event_type = type
        
    def to_dict(self):
        return {"id": self.__event_id,
                "app_id": self.__app_id,
                "task_id": self.__task_ids,
                "arrival_time": self.__arrival_time.strftime(time_format),
                "priority": self.__priority}       
    
    def get_arrival_time(self):
        return self.__arrival_time 
    
    def set_event_id(self, event_id):
        self.__event_id = event_id
        
    def get_app_id(self):
        return self.__app_id
    
    def get_event_type(self):
        return self.__event_type
    
    def get_task_id(self):
        return self.__task_ids
    

class event_queue:
    def __init__(self):
        self.events = []
        self.__event_id = 0
        
    def add_event(self, event):
        event.set_event_id(generate_event_id(self.__event_id))
        self.__event_id = self.__event_id + 1
        
        if not self.events:
            self.events.append(event)
        else:
            for i, e in enumerate(self.events):
                if event.get_arrival_time() < e.get_arrival_time():
                    self.events.insert(i, event)
                    break
            else:
                self.events.append(event)
                
    def remove_next_event(self):
        if self.events:
            return self.events.pop(0)
        else:
            return None
        
    def get_next_event_time(self):
        if self.events:
            return self.events[0].get_arrival_time()
        else:
            return None
        
    def is_empty(self):
        return len(self.events) == 0
    
    def format_csv(self):
        ret = []
        for e in self.events:
            ret.append(e.to_dict())
        return ret
    
    def field_names(self):
        return ["id", "app_id", "task_id", "arrival_time", "priority"]
