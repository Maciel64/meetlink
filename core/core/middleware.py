import datetime
import logging

from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)


class LoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        logger.info(
            f"{datetime.datetime.now()} | Request: {request.method}"
            f"{request.get_full_path()}"
        )

    def process_response(self, request, response):
        logger.info(
            f"{datetime.datetime.now()} | Response: {response.status_code}"
            f"{request.get_full_path()}"
        )
        return response
