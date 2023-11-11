from typing import Union, List, Dict
import pandas as pd

from fastapi import FastAPI

app = FastAPI()

outfit_data = pd.read_csv('../dataset/outfit_data.csv')

def find_outfit_id( product_id):
   return outfit_data.loc[outfit_data['cod_modelo_color'] == product_id, 'cod_outfit'].values

def find_outfit_product_ids(product_id): 
    outfit_ids = find_outfit_id(product_id)

    if(len(outfit_ids) == 0):
        return []
    
    outfit_id = outfit_ids[0]
    return outfit_data.loc[outfit_data['cod_outfit'] == outfit_id, 'cod_modelo_color'].values


@app.get("/")
def read_root():
    return {"Hello": "Mango Fashion Challenge"}


@app.get("/product/{product_id}", response_model=Dict[str, List[str]])
async def read_item(product_id: str):
    product_ids = find_outfit_product_ids(product_id)

    return { "related_products" : product_ids }