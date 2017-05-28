"""This module contains custom exception classes"""


class Error(Exception):
    """An ambiguous exception that occured while executing library code

    This is a base exception for all library exceptions.
    """


class LogsHandlerError(Error):
    """An error occurred inside logging handler"""
