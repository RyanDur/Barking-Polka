import json
import time
from dataclasses import dataclass

from faker import Faker
from fastapi import FastAPI, APIRouter, Request
from starlette.responses import StreamingResponse

app = FastAPI()

router = APIRouter()


@dataclass
class ServerEvent:
    event: str
    data: str
    retry: int = 0

    def __str__(self):
        return f"event:{self.event}\ndata:{self.data}\n\n"


async def data_generator(request: Request):
    fake = Faker()
    next_id = 0
    while not await request.is_disconnected():
        yield str(ServerEvent(event="chat", data=json.dumps({
            "voice": fake.random_element(["friend 1", "friend 2"]),
            "message": f"{fake.sentence()}",
            "id": next_id,
        })))
        time.sleep(1)
        next_id += 1


@router.get("/events")
async def events(request: Request):
    return StreamingResponse(data_generator(request), headers={
        "Content-Type": "text/event-stream",
        "Cache-Control": "no-cache",
        "Access-Control-Allow-Origin": "*"
    })


app.include_router(router, prefix="/api")
