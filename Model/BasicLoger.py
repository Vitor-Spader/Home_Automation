from Interface import ILoger
import datetime

class BasicLoger(ILoger.ILoger):

    def __init__(self, _module_description:str, _path_file:str):
        self.module_description = _module_description
        self.path_file = _path_file

    def write_log(self, _description:str):
        with open(self.path_file,'a') as file:
            file.write(
                {
                    "description": _description,
                    "module": self.module_description,
                    "CreatedDate": datetime.datetime.now()
                }.__str__()
            )