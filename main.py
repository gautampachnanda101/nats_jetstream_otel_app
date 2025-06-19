import asyncio
from nats.aio.client import Client as NATS
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

# Set up OpenTelemetry TracerProvider and OTLP exporter
resource = Resource(attributes={"service.name": "nats-jetstream-app"})
provider = TracerProvider(resource=resource)
trace.set_tracer_provider(provider)
otlp_exporter = OTLPSpanExporter(endpoint="otel-lgtm:4317", insecure=True)
span_processor = BatchSpanProcessor(otlp_exporter)
provider.add_span_processor(span_processor)

tracer = trace.get_tracer(__name__)

async def publish_with_tracing(nc, subject, payload):
    with tracer.start_as_current_span("nats.publish") as span:
        span.set_attribute("messaging.system", "nats")
        span.set_attribute("messaging.destination", subject)
        await nc.publish(subject, payload.encode())

async def message_handler(msg):
    with tracer.start_as_current_span("nats.receive") as span:
        span.set_attribute("messaging.system", "nats")
        span.set_attribute("messaging.destination", msg.subject)
        span.set_attribute("messaging.message_id", msg.reply)
        print(f"Received a message on '{msg.subject}': {msg.data.decode()}")

async def periodic_publisher(nc, subject, interval=2):
    count = 0
    while True:
        message = f"hello world {count}"
        await publish_with_tracing(nc, subject, message)
        print(f"Published: {message}")
        count += 1
        await asyncio.sleep(interval)

async def main():
    nc = NATS()
    await nc.connect("nats://nats:4222")

    # Subscribe with tracing-enabled handler
    await nc.subscribe("foo", cb=message_handler)

    # Start periodic publisher
    await periodic_publisher(nc, "foo")

    # The app will keep running, sending and receiving messages

if __name__ == "__main__":
    asyncio.run(main())