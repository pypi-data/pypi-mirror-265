from testingcgsdk.data_load.read_data.load_data import data_loading
import uvicorn
from fastapi import FastAPI

app = FastAPI()
@app.post("/insert_data_api")
async def insert_data(filename):
    obj = data_loading()
    return (obj._load_csv(filename))

def read_csv(filename):
    obj = data_loading()
    return (obj._load_csv(filename))
    
    #def read_excel(self,filename):
if __name__ == "__main__":
    uvicorn.run("app:app", reload =False, host="127.0.0.1",port=8519)
