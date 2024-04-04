import pandas as pd
from testingcgsdk.data_load.read_data.load_data import data_loading
import uvicorn
from fastapi import FastAPI

app = FastAPI()
@app.post("/insert_data_api")
async def insert_data(filename):
    obj = data_loading()
    return (obj._load_csv(filename))
    

def func1():
    uvicorn.run("app:app", reload =False, host="127.0.0.0",port=8519)
    
