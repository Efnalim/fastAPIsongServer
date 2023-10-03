from fastapi import FastAPI, APIRouter
import uvicorn
from .routers.worship import worship_router
from .routers.hymn import hymn_router
from .routers.login import auth_router

app = FastAPI()
# class HelloWorld():
#     def read_hello(self):
#         return {"data": "Hello Worldo"}
# router = APIRouter()
# router.add_api_route('/api/v2/hello-world', 
# endpoint = HelloWorld().read_hello, methods=["GET"])
app.include_router(worship_router)
app.include_router(hymn_router)
app.include_router(auth_router)

@app.get("/")
def read_root():
    return {"Hello": "World"}

if __name__ == "__main__":
   uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
# from fastapi import FastAPI, APIRouter
# import uvicorn

# from .routers import login, worship, hymn

# app = FastAPI()

# app.include_router(login.router)
# app.include_router(hymn.router)
# app.include_router(worship.router)

# @app.get("/")
# async def root():
#     return {"message": "Gateway of the App"}

# if __name__ == "__main__":
#    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)