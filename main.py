import csv
from typing import Annotated, List

from fastapi import FastAPI, File, UploadFile

import pandas as pd
from pydantic import BaseModel

class Transaction(BaseModel):
    date: str
    currency: str
    type: str
    amount: str
    from_account: str
    to_account: str
    value: str

app = FastAPI()
@app.get("/calculate")
async def root():
    return {"message": "Calculating"}


@app.post("/files/")
async def create_file(file: Annotated[bytes, File()]):
    return {"file_size": len(file)}


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}    


def import_csv_data(content,name):
    data = []
    print("hello",content)
    with open(name, newline='') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        print("csv_reader",csv_reader)
        next(csv_reader)  # Skip the header row if present
        for row in content:
            print("lalua",row['Date'])
            data.append(row)
    print("Data",data)
    return data

@app.post("/excel/")
async def upload_excel_parser(data: List[List[str]]):
    print("data",data)
    df = pd.DataFrame(data, columns=['Date', 'Currency', 'Type', 'Coin', 'Price', 'Fees', 'Total'])
    numeric_columns = ['Coin', 'Price', 'Fees', 'Total']
    df[numeric_columns] = df[numeric_columns].astype(float)
    df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y')
    pivot_table = df.pivot_table(
    index=['Currency', 'Type'],
    values=['Coin', 'Total', 'Fees', 'Price'],
    aggfunc={'Coin': 'sum', 'Total': 'sum', 'Fees': 'sum', 'Price': 'mean'})
    print("Pivot Table:")
    print(pivot_table)
    return df