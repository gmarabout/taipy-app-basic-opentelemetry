import os
import logging
from opentelemetry import metrics
from opentelemetry import trace
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.resources import Resource, SERVICE_NAME
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
)

logging.basicConfig(level=logging.DEBUG)


service_name = os.environ.get("OTEL_SERVICE_NAME", __file__)
otel_endpoint = os.environ.get("OTEL_EXPORTER_OTLP_ENDPOINT", "localhost:4317")

resource = Resource(attributes={SERVICE_NAME: service_name})


###### Metrics
metrics_reader = PeriodicExportingMetricReader(
    OTLPMetricExporter(endpoint=otel_endpoint)
)
metrics_provider = MeterProvider(metric_readers=[metrics_reader], resource=resource)
# Set the global default metrics provider
metrics.set_meter_provider(metrics_provider)

###### Traces
trace_provider = TracerProvider()
processor = BatchSpanProcessor(OTLPSpanExporter(endpoint=otel_endpoint))
trace_provider.add_span_processor(processor)
# Sets the global default tracer provider
trace.set_tracer_provider(trace_provider)

meter = metrics.get_meter_provider().get_meter("my.meter.name")
tracer = trace.get_tracer("my.tracer.name")


def init_metrics() -> dict:
    """Initializes metrics"""
    scenario_execution_counter = meter.create_counter(
        "scenario_execution",
        unit="counts",
        description="Counts the total number of times we execute a scenario",
    )

    rec_svc_metrics = {"scenario_execution_counter": scenario_execution_counter}
    return rec_svc_metrics
