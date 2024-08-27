import time
import threading
from typing import Dict


class Scheduler:
    def __init__(self, period=0.3):
        self.active = False
        self.period = period
        self._main_events = dict()
        
        self.timer = threading.Timer(self.period, self.fixed_update)
        self._fixed_events = dict()
        self.fixed_results = []
    
    def update(self):
        result = dict()
        if self.active == False:
            return result
        
        for name, event in self._main_events.items():
            result[name] = event()
        return result
    
    def fixed_update(self):
        begin = time.time()
        result = dict()
        if self.active == False:
            return
        
        for name, event in self._fixed_events.items():
            result[name] = event()
        self.fixed_results.append(result)
        if time.time() - begin > self.period:
            self.period = time.time() - begin
        self.timer = threading.Timer(self.period, self.fixed_update)
        self.timer.start()
            
    def run(self)->Dict[str, object]:
        self.active = True
        self.timer.start()
        return dict()
    
    def stop(self)->Dict[str, object]:
        self.active = False
        self.timer.cancel()
        return dict()
    
    def add_event(self, event, name):
        if name in self._main_events or name in self._fixed_events:
            return None
        self._main_events[name] = event
        
    def add_fixed_event(self, event, name):
        if name in self._main_events or name in self._fixed_events:
            return None
        self._fixed_events[name] = event
    
    def del_event(self, name):
        if name in self._main_events:
            del self._main_events[name]
        if name in self._fixed_events:
            del self._fixed_events[name]
            