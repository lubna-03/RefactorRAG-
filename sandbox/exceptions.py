class UnauthorizedError(Exception):
    pass

class BadRequestError(Exception):
    pass

class PaymentGatewayError(Exception):
    pass

class ReportStorageError(Exception):
    pass
