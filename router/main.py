from fastapi import FastAPI, APIRouter
import uvicorn

app = FastAPI()
class HelloWorld():
    def read_hello(self):
        return {"data": "Hello World"}
router = APIRouter()
router.add_api_route('/api/v2/hello-world', 
endpoint = HelloWorld().read_hello, methods=["GET"])
app.include_router(router)

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