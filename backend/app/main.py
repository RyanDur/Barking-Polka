import asyncio
import json
import uuid
from dataclasses import dataclass

from faker import Faker
from fastapi import FastAPI, APIRouter, Request
from starlette.responses import StreamingResponse

app = FastAPI()

router = APIRouter()


@dataclass
class Message:
    voice: str
    message: str
    id: str

    def __str__(self):
        return json.dumps({"voice": self.voice, "message": self.message, "id": self.id})


@dataclass
class ServerEvent:
    event: str
    data: Message

    def __str__(self):
        return f"event:{self.event}\ndata:{self.data}\n\n"


async def data_generator(request: Request):
    fake = Faker()
    while not await request.is_disconnected():
        yield str(ServerEvent(event="chat", data=Message(
            voice=fake.random_element(["friend 1", "friend 2"]),
            message=fake.sentence(),
            id=uuid.uuid4().hex,
        )))
        await asyncio.sleep(10)


@router.get("/events")
async def events(request: Request):
    return StreamingResponse(data_generator(request), headers={
        "Content-Type": "text/event-stream",
        "Cache-Control": "no-cache",
        "Access-Control-Allow-Origin": "*"
    })


app.include_router(router, prefix="/api")
