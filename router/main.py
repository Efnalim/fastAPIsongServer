from fastapi import FastAPI, APIRouter
import uvicorn

from routers.song_router import SongRouter

app = FastAPI()
class HelloWorld():
    def read_hello(self):
        return {"data": "Hello World"}
    

router = APIRouter()
router.add_api_route('/api/v2/hello-world', endpoint = HelloWorld().read_hello, methods=["GET"])
router.add_api_route('/songs', endpoint = SongRouter().getAllSongs, methods=["GET"])

app.include_router(router)

if __name__ == "__main__":
   uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)