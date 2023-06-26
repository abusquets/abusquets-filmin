from shared.exceptions import APPException


class EmptyPayloadException(APPException):
    status_code = 422
    code = 'empty-payload'
    message = "You haven't sent any data"
