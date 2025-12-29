from fastapi import FastAPI, Request, Response
import example_pb2
import time

app = FastAPI()


@app.post("/hello")
async def hello(request: Request):
    
    # Read raw protobuf bytes
    body = await request.body()

    # Decode protobuf
    req = example_pb2.HelloRequest()
    req.ParseFromString(body)

    # Business logic
    resp = example_pb2.HelloResponse()
    resp.message = f"Hello, {req.name}!"

    # Encode protobuf response
    return Response(
        content=resp.SerializeToString(),
        media_type="application/x-protobuf"
    )

