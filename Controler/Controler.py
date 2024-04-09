from Interface import IBoard, IDatabase, IEvent
import uuid

class Controler:
    def __init__(self, _board:IBoard.IBoard, _event:IEvent.IEvent, _database:IDatabase=None):
        self.board = _board
        self.event = _event
        self.id = uuid.uuid4()

    def turn_on(self, _id:[int]):
        self.__verify_list__(_id)
        self.board.set_on(_id)

    def turn_off(self, _id:[int]):
        self.__verify_list__(_id)
        self.board.set_off(_id)

    def switch(self, _id:[int]):
        self.__verify_list__(_id)
        self.board.switch(_id)

    async def set_alarm_on(self):
        await self.event.start_event()

    def set_alarm_off(self, _id):
        pass

    def get_state(self, _id):
        self.__verify_list__(_id)
        return self.board.get_state(_id)
    
    def __verify_list__(self, list_to_verify:[]):
        if list_to_verify is None:
            raise Exception('Invalid parameters of ligths')
    
    def get_id(self) -> str:
        return str(self.id)

    def close(self):
        self.board.close()