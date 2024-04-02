import pandas as pd
from testingcgsdk.data_load.read_data.load_data import data_loading


app = FastAPI()
@app.post("/insert_data_api")
def insert_data(filename):
    obj = data_loading()
    return (obj._load_csv(filename))
    


