from confluent_kafka import Consumer, Producer
import example_pb2

# Kafka config
consumer_conf = {
    "bootstrap.servers": "localhost:29099",
    "group.id": "hello-service",
    "auto.offset.reset": "earliest",
}

producer_conf = {
    "bootstrap.servers": "localhost:29099",
}

consumer = Consumer(consumer_conf)
producer = Producer(producer_conf)

consumer.subscribe(["hello-requests"])

print("🚀 Hello service started (Kafka)")

try:
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            print("Consumer error:", msg.error())
            continue

        # Decode protobuf request
        req = example_pb2.HelloRequest()
        req.ParseFromString(msg.value())

        print(f"📥 Received request: {req.name}")

        # Business logic
        resp = example_pb2.HelloResponse()
        resp.message = f"Hello, {req.name}!"

        # Send response
        producer.produce(
            topic="hello-responses",
            value=resp.SerializeToString(),
        )
        producer.flush()

except KeyboardInterrupt:
    pass
finally:
    consumer.close()
