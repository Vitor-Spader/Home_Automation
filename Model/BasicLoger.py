from Interface import ILoger
import datetime
import json

class BasicLoger(ILoger.ILoger):

    def __init__(self, _module_description:str, _path_file:str):
        self.module_description = _module_description
        self.path_file = _path_file

    def write_log(self, _description:str): 
        try: 
            with open(self.path_file,'a') as file:
                json_file = json.loads(file.readlines())
                json_file.append({
                                    "description": _description,
                                    "module": self.module_description,
                                    "CreatedDate": datetime.datetime.now().__str__()
                                })
                json.dump(json_file, file, indent = 6)
        except:
            json.dump({
                                    "description": _description,
                                    "module": self.module_description,
                                    "CreatedDate": datetime.datetime.now().__str__()
                                }, file, indent = 6)