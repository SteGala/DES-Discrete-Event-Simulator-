class priority(enumerate):
    LOW = 0
    HIGH = 1

class event:
    def __init__(self, event_id, app_id, task_id, arrival_time, priority):
        self.__event_id = event_id
        self.__app_id = app_id
        self.__task_id = task_id
        self.__arrival_time = arrival_time
        self.__priority = priority
        
    def to_dict(self):
        return {"id": self.__event_id,
                "app_id": self.__app_id,
                "task_id": self.__task_id,
                "arrival_time": self.__arrival_time,
                "priority": self.__priority}       
    
    def get_arrival_time(self):
        return self.__arrival_time 

class event_queue:
    def __init__(self):
        self.events = []
        
    def add_event(self, event):
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
