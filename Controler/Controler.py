from Interface import IBoard, IDatabase, IAlarm

class Controler:
    def __init__(self, _board:[IBoard.IBoard], _alarm:IAlarm, _database:IDatabase=None):
        self.board = _board
        self.alarm = _alarm

    def turn_on(self, _id_board, _id):
        pass
    def turn_off(self, _id_board, _id):
        pass
    def switch(self, _id_board, _id):
        pass
    def set_alarm_on(self, _id):
        pass
    def set_alarm_off(self, _id):
        pass
    def get_state(self, _id_board, _id):
        pass
    