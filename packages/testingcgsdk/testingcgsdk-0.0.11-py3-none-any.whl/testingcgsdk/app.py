import pandas as pd
from testingcgsdk.data_load.read_data.load_data import data_loading
from fastapi import FastAPI
import uvicorn

app = FastAPI()
@app.post("/insert_data_api")
def insert_data(filename):
    obj = data_loading()
    return (obj._load_csv(filename))

if __name__ == "__main__":
    uvicorn.run("app:app", reload =False, host="127.0.0.1",port=8519)
    


