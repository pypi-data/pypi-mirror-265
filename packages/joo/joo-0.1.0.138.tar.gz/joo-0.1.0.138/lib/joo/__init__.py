"""
    This file is part of joo library.
    :copyright: Copyright 1993-2024 Wooloo Studio.  All rights reserved.
    :license: MIT, check LICENSE for details.
"""
import time
from abc import ABC, abstractmethod

class ManagedObject:
    def __init__(self):
        self._state = None

    def __del__(self):
        if self._state != None:
            raise Exception("Object must be released explicitly.")
        
    @property
    def state(self): return self._state

class ManagedObjects(ABC):
    def __init__(self):
        self._objects = []

    def register_object(self, obj):
        if obj not in self._objects: self._objects.append(obj)

    def unregister_object(self, obj):
        while obj in self._objects: self._objects.remove(obj)

    def gc(self):
        # assume object supports the delete(gc) method
        # gc=True means it's in gc() process, so should not make
        # any call of register_object() or unregister_object().
        for obj in self._objects: obj.delete(gc=True)
        self._objects.clear()

class DebugTimer:
    def __init__(self):
        self._checkpoints = []
        self.reset()

    def reset(self):
        self._checkpoints.clear()
        self.record()

    def record(self, finished_step_label=""):
        self._checkpoints.append((time.perf_counter(), finished_step_label))

    def __enter__(self):
        self.reset()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.record()
        
    def get_results(self):
        if len(self._checkpoints) <= 1: return None
        results = []
        base_ts = 0.0
        last_ts = None
        for (ts, label) in self._checkpoints:
            if last_ts is None:
                base_ts = ts
            else:
                results.append((label, ts - last_ts, ts - base_ts))
            last_ts = ts
        return results
    
    def get_step_duration(self, step_label=None):
        results = self.get_results()
        if results is None: return None
        if step_label is None:
            return results[-1][2]  # total duration
        else:
            for (label, step_duration, process_duration) in results:
                if label == step_label: return step_duration
        return None
    
    def format_results(self, show_step_percentage=False, show_total_duration=False):
        results = self.get_results()
        if results is None: return ""
        
        # steps
        t = ""
        total_duration = results[-1][2]
        index = 1
        for (label, step_duration, process_duration) in results:
            step_label = label if label != "" else "(#{})".format(index)
            if t != "": t += "\r\n"
            t += "{}: {:.4f} seconds".format(step_label, step_duration)
            if show_step_percentage and total_duration > 0.0:
                t += " ({:.2f}%)".format(step_duration / total_duration * 100.0)
            index += 1
        
        # total
        if show_total_duration:
            t += "\r\nTotal: {:.4f} seconds".format(total_duration)
        #
        return t
    
class DebugBlock:
    def __init__(self, name, logger=None, mode="b/e"):
        self.name = name
        self.logger = logger
        if mode in ["b/e", "begin/end"]:
            self.verbs = ("Begin", "End")
        elif mode in ["s/e", "start/end"]:
            self.verbs = ("Start", "End")
        elif mode in ["o/c", "open/close"]:
            self.verbs = ("Open", "Close")
        elif mode in ["e/l", "enter/leave"]:
            self.verbs = ("Enter", "Leave")
        else:
            self.verbs = ("", "")

    def __enter__(self):
        text = ">>>>>>>> {} >>>>>>>>".format((self.verbs[0] + " " + self.name).strip())
        if self.logger:
            self.logger.debug(text)
        else:
            print(text)

    def __exit__(self, exc_type, exc_val, exc_tb):
        text = "<<<<<<<< {} <<<<<<<<".format((self.verbs[1] + " " + self.name).strip())
        if self.logger:
            self.logger.debug(text)
        else:
            print(text)