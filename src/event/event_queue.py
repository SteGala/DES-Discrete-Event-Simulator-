class priority(enumerate):
    LOW = 0
    HIGH = 1

class event:
    def __init__(self, app_id, task_id, arrival_time, priority):
        self.__app_id = app_id
        self.__task_id = task_id
        self.__arrival_time = arrival_time
        self.priority = priority

class event_queue:
    def __init__(self):
        self.events = []
        
    def add_event(self, event):
        if not self.events:
            self.events.append(event)
        else:
            for i, e in enumerate(self.events):
                if event.__arrival_time < e.__arrival_time:
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
            return self.events[0].arrival_time
        else:
            return None
        
    def is_empty(self):
        return len(self.events) == 0
