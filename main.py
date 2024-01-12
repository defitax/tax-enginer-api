from fastapi import FastAPI
app = FastAPI()
@app.get("/calculate")
async def root():
    return {"message": "Calculating"}