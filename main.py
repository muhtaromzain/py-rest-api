from typing import Union
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import time

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class ReturnException(BaseModel):
    detail: str

class Return200(BaseModel):
    status: str
    startTime: str
    endTime: str
    duration: str

class Return406(BaseModel):
    status: str
    message: str

def repetition(n: int)-> dict:
    # Record the start time
    startTime = time.time()

    # Loop through (n) times
    for i in range(n):
        pass

    # Record the end time
    endTime = time.time()

    # Calculate the duration
    duration = endTime - startTime
    duration = round(duration, 4)

    # Print the start time, end time, and duration
    print(f"Start Time: {startTime}")
    print(f"End Time: {endTime}")
    print(f"Duration: {duration} seconds")

    return {
        "startTime": startTime,
        "endTime": endTime,
        "duration": duration
    }

@app.get("/loops/{loopNumber}", status_code=200, responses={
    201: {
        "model": Return200
    },
    406: {
        "model": Return406
    },
    409: {
        "model": ReturnException
    }
}
)
def run_loops(loopNumber: int, q: Union[str, None] = None):
    maxLoops = 100_000_000
    if loopNumber > maxLoops:
        raise HTTPException(
            status_code=406, detail='Loops limit reached'
        )
        
    try:
        loops = repetition(loopNumber)
        return Return200(status="Success", startTime=loops["startTime"], endTime=loops["endTime"], duration=loops["duration"])
    except:
        raise HTTPException(
            status_code=409, detail='Failed'
        )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)