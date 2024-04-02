import datetime
from pydantic import BaseModel
from Controler import Controler
from fastapi import FastAPI
from Interface import IBoard, IEvent
from Model import Event
import platform

board:IBoard.IBoard

if platform.machine() == 'armv7l':
    from Model import Raspberry
    board = [Raspberry.Raspberry(_list_input=[2],_list_output=[17],_list_relationship=[None,[17]])]
else:
    from Model import TestIO
    board = [TestIO.TestIO(_list_input=[2],_list_output=[17],_list_relationship=[None,[17]])]

controler = Controler.Controler(board,
                                Event.Event(None, datetime.time(6,0,0),Event.Event.EVERY_DAY,(lambda :board.set_on([17])))) 
del board
app = FastAPI()

#Modelos de dados a serem recebidos pela API
class Light(BaseModel):
    Id_board: int
    Id:list|int

#Definição de métodos e paths permitidos
@app.post("/turn_on")
def request_turn_on(Light:Light):
    return {"Succesful": controler.turn_on(_id_board=Light.Id_board, _id=Light.Id)}

#Definição de métodos e paths permitidos
@app.post("/turn_off")
def request_turn_off(Light:Light):
    return {"Succesful": controler.turn_off(_id_board=Light.Id_board, _id=Light.Id)}

#Definição de métodos e paths permitidos
@app.post("/switch")
def request_refresh_database(Light:Light):
    return {"Succesful": controler.switch(_id_board=Light.Id_board, _id=Light.Id)}

@app.post("/state")
def request_read_item(Light:Light):
    return {"state":controler.get_state(_id_board=Light.Id_board, _id=Light.Id)}
