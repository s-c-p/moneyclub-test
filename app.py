import os
import sys
from fastapi import FastAPI

app = FastAPI()

if os.getenv("FAST", default=False):
    from pythonic_be import main
else:
    from sql_be import main
 
@app.get("/")
def root()
