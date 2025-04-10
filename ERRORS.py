class ZeroError(Exception):
    pass


class ErrorInRMortgageS(Exception):
    pass


class ErrorInCredit(Exception):
    pass


class ErrorInRMortgageM(Exception):
    pass


class ErrorLargeNumber(Exception):
    pass


class PercentError(ErrorInRMortgageS, ErrorInRMortgageM, ErrorInCredit):
    pass


class ErrorInMonth(ErrorInRMortgageS, ErrorInCredit):
    pass


class ErrorInYear(ErrorInRMortgageS):
    pass


class ErrorMortgageAmount(ErrorInRMortgageS, ErrorInRMortgageM, ErrorInCredit):
    pass


class ErrorMonthlyPayment(ErrorInRMortgageM):
    pass


class ErrorInitialFee(ErrorInRMortgageS, ErrorInRMortgageM):
    pass
