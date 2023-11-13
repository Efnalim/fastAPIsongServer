from fastapi import FastAPI, APIRouter
import uvicorn
from routers.worship import worship_router
# from .routers.hymn import hymn_router
# from .routers.login import auth_router

app = FastAPI()
app.include_router(worship_router)
# app.include_router(hymn_router)
# app.include_router(auth_router)

@app.get("/")
def read_root():
    return {"Hello": "World"}

if __name__ == "__main__":
   uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
   