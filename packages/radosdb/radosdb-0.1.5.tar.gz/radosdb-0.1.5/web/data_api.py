import pandas as pd
from fastapi import FastAPI
from typing import Dict, Any
import numpy as np

from radosdb.database_api import write_df

app = FastAPI()

@app.put("/name/{name}")
def update_data(name: str, data: Dict[str, Any]):
    data = pd.DataFrame(data)
    data.index = pd.to_datetime(data.index)
    data = data.replace('null',np.nan)
    data = data.astype('float64')
    res = write_df(name, data, freq=20,start=None,end=None)
    if res==0:
        print(name)
        return True
    else:
        return False



if __name__ == "__main__":
    import uvicorn
    uvicorn.run("data_api:app", host="0.0.0.0", port=50051)