# https://docs.djangoproject.com/en/5.2/topics/http/middleware/
from logging import getLogger


class LoggingMiddleware:

    HTTP_LOGGING_TEMPLETE = """
    {method}: {path} 
    {headers}: {body}
    {exception}
    """

    def __init__(self, get_response):
        self.logger = getLogger(self.__class__.__name__)
        self.get_response = get_response

    def __call__(self, request):

        before_request_str = (
            LoggingMiddleware.HTTP_LOGGING_TEMPLETE.format(
                method=str(request.method),
                path=str(request.path),
                headers=str(request.META),
                body=str(request.body),
                exception=str(),
            )
        )
        self.logger.info(before_request_str)
        response = self.get_response(request)

        after_request_str = (
            LoggingMiddleware.HTTP_LOGGING_TEMPLETE.format(
                method=str(request.method),
                path=str(request.path),
                headers=str(response.headers),
                body=str(response.content),
                exception=str(),
            )
        )

        self.logger.info(after_request_str)

        return response

    def process_exception(self, request, exception):

        exception_str = (
            LoggingMiddleware.HTTP_LOGGING_TEMPLETE.format(
                method=str(request.method),
                path=str(request.path),
                headers=str(request.META),
                body=str(request.body),
                exception=str(exception),
            )
        )

        self.logger.error(exception_str, exc_info=True)

        # should return None to process
