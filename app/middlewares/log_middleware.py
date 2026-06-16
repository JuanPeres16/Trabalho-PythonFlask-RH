from time import perf_counter

from flask import g, request

from app.services.log_service import LogService


def init_log_middleware(app):
    @app.before_request
    def start_timer():
        g.request_started_at = perf_counter()

    @app.after_request
    def log_request(response):
        if request.path.startswith("/static"):
            return response

        elapsed_ms = round((perf_counter() - g.get("request_started_at", perf_counter())) * 1000, 2)
        LogService().save_access_log(response, elapsed_ms)
        return response
