from confluent_kafka import Producer, Consumer
import example_pb2
import time

producer_conf = {
    "bootstrap.servers": "localhost:29099",
}

consumer_conf = {
    "bootstrap.servers": "localhost:29099",
    "group.id": "hello-client",
    "auto.offset.reset": "earliest",
}

producer = Producer(producer_conf)
consumer = Consumer(consumer_conf)

consumer.subscribe(["hello-responses"])

names = [
    "Viet", "Edmond", "Jinx", "Jhin",
    "Vayne", "Draven", "Lucian", "Aphelios"
]

# Send requests
for name in names:
    req = example_pb2.HelloRequest()
    req.name = name

    producer.produce(
        topic="hello-requests",
        value=req.SerializeToString(),
    )
    producer.flush()
    print(f"📤 Sent request: {name}")

# Receive responses
received = 0
while received < len(names):
    msg = consumer.poll(5.0)
    if msg is None:
        continue
    if msg.error():
        print("Consumer error:", msg.error())
        continue

    resp = example_pb2.HelloResponse()
    resp.ParseFromString(msg.value())
    print(f"📥 Response: {resp.message}")

    received += 1

consumer.close()
