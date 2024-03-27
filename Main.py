from pydantic import BaseModel
from Controler import Controler
from fastapi import FastAPI
from Model import Board, Raspberry, Test_IO

DATABASE = csv_database.csv_database(CSV_PATH)

View_Control = View_Control.View_Control(_database=DATABASE)
app = FastAPI()

#Modelos de dados a serem recebidos pela API
class Light(BaseModel):
    Id_board: str
    Id:int

#Definição de métodos e paths permitidos
@app.post("/turn_on")
async def refresh_database(Light:Light):
    return {"Succesful": Scrapping.Table(Url.Url,DATABASE).load()}

#Definição de métodos e paths permitidos
@app.post("/turn_off")
async def refresh_database(Light:Light):
    return {"Succesful": Scrapping.Table(Url.Url,DATABASE).load()}

#Definição de métodos e paths permitidos
@app.post("/switch")
async def refresh_database(Light:Light):
    return {"Succesful": Scrapping.Table(Url.Url,DATABASE).load()}

@app.post("/state")
def read_item(Light:Light):
    return View_Control.get(id)
