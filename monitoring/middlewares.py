# middleware.py

import logging

logger = logging.getLogger(__name__)

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Log the request path and method
        # Log the request protocol and headers
        logger.info(f"Request Protocol: {request.scheme.upper()}")
        logger.info("Request Headers:")
        for header, value in request.headers.items():
            logger.info(f"{header}: {value}")
        logger.info(f"Incoming request: {request.method} {request.path}")
        
        print(f"Request Protocol: {request.scheme.upper()}")
        print("Request Headers:")
        for header, value in request.headers.items():
            print(f"{header}: {value}")
        print(f"Incoming request: {request.method} {request.path}")

        # Pass the request to the next middleware or view
        response = self.get_response(request)

        return response
