import copy
from typing import Dict
from scheduler.base import Scheduler


class CyclicScheduler(Scheduler):
    def __init__(self, period, cycles=100):
        self.cycles = cycles
        super(CyclicScheduler, self).__init__(period)
    
    def run(self)->Dict[str, object]:
        super(CyclicScheduler, self).run()
        
        main_results = []
        for _ in range(self.cycles):
            main_results.append(self.update())
        
        fixed_results = copy.deepcopy(self.fixed_results)
        self.fixed_results = []
        return {'main': main_results, 'fixed': fixed_results}
    
    def stop(self) -> Dict[str, object]:
        super(CyclicScheduler, self).stop()
        fixed_results = copy.deepcopy(self.fixed_results)
        self.fixed_results = []
        return {'fixed': fixed_results}