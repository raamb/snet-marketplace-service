from common.exceptions import CustomException, MethodNotImplemented


class BadRequestException(CustomException):
    error_message = "BAD_REQUEST"

    def __init__(self):
        super().__init__({})


class OrganizationNotFoundException(CustomException):
    error_message = "ORGANIZATION_NOT_FOUND"

    def __init__(self):
        super().__init__({})


class InvalidOrigin(CustomException):
    error_message = "SERVICE_PROTO_NOT_FOUND"

    def __init__(self):
        super().__init__({})


class InvalidServiceState(CustomException):
    error_message = "INVALID_SERVICE_STATE"

    def __init__(self):
        super().__init__({})


class ServiceProtoNotFoundException(CustomException):
    error_message = "SERVICE_PROTO_NOT_FOUND"

    def __init__(self):
        super().__init__({})


class OrganizationNotPublishedException(CustomException):
    error_message = "ORGANIZATION IS NOT PUBLISHED"

    def __init__(self):
        super().__init__({})


class ServiceNotFoundException(CustomException):
    error_message = "SERVICE_NOT_FOUND"

    def __init__(self):
        super().__init__({})


class ServiceGroupNotFoundException(CustomException):
    error_message = "SERVICE_GROUP_NOT_FOUND"

    def __init__(self):
        super().__init__({})


EXCEPTIONS = (BadRequestException, OrganizationNotFoundException, MethodNotImplemented)
