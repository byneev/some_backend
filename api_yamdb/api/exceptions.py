from rest_framework.exceptions import APIException


class AlreadyExistException(APIException):
    status_code = 500
    default_detail = "User already exists"
