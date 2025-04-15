import prometheus_client as prom
from typing import Dict

class ModelMetrics:
    def __init__(self):
        self.request_count = prom.Counter(
            'model_request_total',
            'Total model inferences',
            ['model_name']
        )
        self.latency = prom.Histogram(
            'model_latency_seconds',
            'Model inference latency',
            ['model_name']
        )
        self.error_count = prom.Counter(
            'model_errors_total',
            'Total model errors',
            ['model_name']
        )

    def track(self, model_name: str):
        def decorator(f):
            def wrapper(*args, **kwargs):
                self.request_count.labels(model_name).inc()
                with self.latency.labels(model_name).time():
                    try:
                        return f(*args, **kwargs)
                    except Exception:
                        self.error_count.labels(model_name).inc()
                        raise
            return wrapper
        return decorator

metrics = ModelMetrics()