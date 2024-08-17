from django.http import JsonResponse
from . import ins_logger
import sys
from django.shortcuts import redirect
from django.urls import resolve


class JWTTokenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_url = resolve(request.path_info).url_name

        if current_url not in ['login', 'signup']:
            token = request.COOKIES.get('access_token')
            if token:
                request.META['HTTP_AUTHORIZATION'] = f'Bearer {token}'
        response = self.get_response(request)
        return response


class CustomExceptionHandlerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = None
        try:
            response = self.get_response(request)
            current_url = resolve(request.path_info).url_name

            if response and response.status_code == 401 and current_url not in ['login', 'signup']:
                return self.handle_unauthorized(request)

            elif response and response.status_code == 404:
                return self.handle_not_found(request)

            elif response and response.status_code >= 400:
                self.log_error(response)

        except Exception as e:
            self.log_exception(e)

        return response

    def handle_unauthorized(self, request):
        if request.is_ajax() or 'application/json' in request.headers.get('Accept', ''):
            return JsonResponse({'error': 'Unauthorized access'}, status=401)
        else:
            return redirect('login')

    def handle_not_found(self, request):
        if request.is_ajax() or 'application/json' in request.headers.get('Accept', ''):
            return JsonResponse({'error': 'Resource not found'}, status=404)
        else:
            return redirect('login')

    def log_error(self, response):
        exc_type, exc_value, exc_traceback = sys.exc_info()
        if exc_traceback:
            ins_logger.logger.error(
                str(response.data), 
                extra={'details': 'line no: ' + str(exc_traceback.tb_lineno)}
            )
        else:
            ins_logger.logger.error(
                str(response.data), 
                extra={'details': 'No traceback available'}
            )

    def log_exception(self, exception):
        exc_type, exc_value, exc_traceback = sys.exc_info()
        if exc_traceback:
            ins_logger.logger.error(
                str(exception), 
                extra={'details': 'line no: ' + str(exc_traceback.tb_lineno)}
            )
        else:
            ins_logger.logger.error(
                str(exception), 
                extra={'details': 'No traceback available'}
            )