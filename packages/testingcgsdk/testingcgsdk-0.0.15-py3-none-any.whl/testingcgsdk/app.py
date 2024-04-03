import pandas as pd
from testingcgsdk.data_load.read_data.load_data import data_loading
from fastapi import FastAPI
import uvicorn


app = FastAPI()
@app.post("/insert_data_api")
async def insert_data(filename):
    obj = data_loading()
    return (obj._load_csv(filename))

async def start_server():
    print("Inside the main for testing")
    uvicorn.run("app:app", reload =False, host="127.0.0.1",port=8519)
    


