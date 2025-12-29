import requests
import example_pb2


# Create request message
req = example_pb2.HelloRequest()

# For loop to simulate stream of requests
names = ["Viet", "Edmond", "Jinx", "Jhin", "Vayne", "Draven", "Lucian",
         "Aphelios"]
for name in names:
    req.name = name

    # Serialise to protobuf bytes
    data = req.SerializeToString()

    # Send HTTP request
    response = requests.post(
        "http://localhost:8000/hello",
        data=data,
        headers={
            "Content-Type": "application/x-protobuf"
        }
    )

    # Decode protobuf response
    resp = example_pb2.HelloResponse()
    resp.ParseFromString(response.content)

    print(resp.message)
