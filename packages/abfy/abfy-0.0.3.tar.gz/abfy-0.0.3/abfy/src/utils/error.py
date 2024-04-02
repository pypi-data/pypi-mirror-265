# Definition of all abfy specific exceptions


class DashABException(Exception):
    """
    All DashAB Exceptions need to be derived from this base class
    """

    def __init__(self, value):
        self.value = value
        super().__init__(value)

    def __str__(self):
        return self.value


class InputConfigError(DashABException):
    # Exceptions related to input DashAB config
    pass


class InputDataError(DashABException):
    # Exceptions related to input data
    pass
