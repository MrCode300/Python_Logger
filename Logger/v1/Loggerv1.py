from datetime import datetime
import time 
import inspect
# Logger 
class Logger:
    def __init__(self): 
        print("started")
        print("  ")
        self.config = {
            "minimum_level": {
                "debug": False,
                "info": True,
                "warning": True,
                "error": True #errors never turn off so this does not do anything 
                }, 
                #this is the defalt of what you can log
                "console_enabled": True, # output to console
                "console_flush_mode": "buffered", #will output at end of program or "immediate"
                "file_enabled": False, #output to file
                "file_path": None, #file that logs output to 
                "file_flush_mode": "immediate", # will output when log is created or "buffered"
                "location_rules": {
                    "debug": False,
                    "info": False,
                    "warning": True,
                    "error": True 
                    
                }, 
                "error_policy": "log_only" # can be recover, exit, or custom 
                } 
        self.debug_logs = {}
        self.info_logs = {} 
        self.warning_logs = {} 
        self.error_logs = {}                 
        self.current_log_id = 0
        self.start_time = time.time()
        
    def _logid_increment(self):
        current_id = self.current_log_id
        self.current_log_id += 1
        return current_id
        
    def _location_get(self):
        locations = {}
        loction_amount = 0
        stack = inspect.stack()
        for frame in stack: 
            if frame.function not in ("_location_get", "_log"): # when I new class function uses loction add it to the list
                locations[loction_amount] = { "filename": frame.filename, "function": frame.function, "line": frame.lineno }
                loction_amount += 1
        return locations
        
    def _log(self, level, message, context=None, location=None, exception=None):
        level = str(level).lower() 
        if level not in self.config["minimum_level"].keys():
            return False
        if self.config["minimum_level"][level] == False and level != "error":
            return False
        if location == None and self.config["location_rules"][level] != False:
            location = self._location_get()
            origin = "automatic"
        elif location != None: origin = "manual"
        if context != None and type(context) is not dict:
            context = None # Also log a warning but I will do that later when I have this working
        id = self._logid_increment()
        record = {
            "metadata": {
                "id": id,
                "level": level,
                "timestamp": datetime.now().isoformat(),
                "uptime": time.time() - self.start_time,
                "origin": origin, "locations": location 
            }, 
            "content": {
                "message": message,
                "context": context
                },
                "error_location": None, #because I have not created that part of the code
                "error": None #because I have not created that part of the code 
                }
        print(record)
