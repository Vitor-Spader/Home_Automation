import datetime
from pydantic import BaseModel
from Controler import Controler
from fastapi import FastAPI
from Interface import IBoard, IEvent
from Model import Event, BasicLoger
import platform

if platform.machine() in ['armv7l','aarch64']:
    from Model import Raspberry
    board = Raspberry.Raspberry(_list_input=[2],
                                 _list_output=[17],
                                 _list_relationship={2:[17]},
                                 _loger=BasicLoger.BasicLoger('Raspberry','log.txt'))
else:
    from Model import TestIO
    board = TestIO.TestIO(_list_input=[2],_list_output=[17],_list_relationship=[None,[17]])

controler = Controler.Controler(board,
                                Event.Event(None, datetime.time(6,0,0),Event.Event.EVERY_DAY,(lambda :board.set_on([17])))) 
del board
app = FastAPI()

#Definição de métodos e paths permitidos
@app.post("/turn_on?q={_id}")
def request_turn_on(_id:int):
    return {"Succesful": controler.turn_on(_id=_id)}

#Definição de métodos e paths permitidos
@app.post("/turn_off?q={_id}")
def request_turn_off(_id:int):
    return {"Succesful": controler.turn_off(_id=_id)}

#Definição de métodos e paths permitidos
@app.post("/switch?q={_id}")
def request_refresh_database(_id:int):
    return {"Succesful": controler.switch(_id=_id)}

@app.post("/state?q={_id}")
def request_read_item(_id:int):
    return {"state":controler.get_state(_id=_id)}

@app.get("/get_id")
def request_get_id():
    return controler.get_id()

@app.get("/close")
def request_close():
    return controler.close()
