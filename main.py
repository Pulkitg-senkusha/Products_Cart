from fastapi import FastAPI
from api.routes import router
import uvicorn
import os
from dotenv import load_dotenv
from database.connections import init_db 
from logger import logger  
load_dotenv()

init_db()

app = FastAPI(title="E-Commerce Products")
app.include_router(router)


@app.get("/")
def read_root():
    logger.info("Root endpoint was accessed.")
    return {"message": "Hello World"}

host = os.getenv("HOST", "localhost")
port = int(os.getenv("PORT", 8000))   

if __name__ == "__main__":
    uvicorn.run("main:app", host=host, port=port, reload=True)
