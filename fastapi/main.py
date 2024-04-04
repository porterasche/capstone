from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
# pip install fastapi[all]

app.add_middleware(
    CORSMiddleware, # SHOULD SPECIFY EXACT ORIGIN FOR PROPER SECURITY
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/process")
async def process(field1: str = Query(None), field2: str = Query(None), field3: str = Query(None)):
    # Do some work with the received values
    result = "Result From FastAPI Server"

    # Send a response back to the UI
    return {"message": f"Processed: field1={field1}, field2={field2}, field3={field3}, result={result}"}

@app.get("/run_algorithm")
async def run_algorithm(field1: str = Query(None), field2: str = Query(None), field3: str = Query(None)):
    # return list of 3 classes
    return [{
        "id": "CSCI1620"
    }, {
        "id": "CSCI4350"
    }, {
        "id": "CSCI4560"
    }]