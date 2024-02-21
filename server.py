## not in use.. can be refactored later

from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/request/{userRequest}")
def read_item(userRequest: str):
    ## TO DO - Ask openAI to look at our user's request
    return {"response": "The user asked for " + userRequest}
