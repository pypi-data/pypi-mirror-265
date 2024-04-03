# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-import

# from dataclasses import dataclass
# from typing import Iterable, OrderedDict, Union
# from collections import OrderedDict
# from abc import ABC, abstractmethod
import re

import colemen_utils as c

import volent.settings as _settings
import volent.settings.types as _t
from volent.exceptions import ValidationError
from volent.validate.Validator import Validator

class LessThan(Validator):

    field_name = None
    default_message = "Must be Less than {comparable}"


    def __init__(
        self,
        comparable,
        inclusive=False,
        ):
        '''
        Validate that the comparable is less than the value.

        Arguments
        ----------------

        `comparable` {int,float}
            The value must be less than (or equal to) this value

        `inclusive` {bool} = False
            If True the value can be less than or eqaul to the comparable.
        '''
        self.comparable = comparable
        self.inclusive = inclusive


    def _format_error(self,value) -> str:
        if self.field_name is not None:
            if self.inclusive is True:
                return  f"{self.field_name} must be less than or equal to {self.comparable}"
            return  f"{self.field_name} must be less than {self.comparable}"
        return self.default_message.format(input=value, comparable=self.comparable)

    def _repr_args(self) -> str:
        return f"comparable={self.comparable!r}"

    def __call__(self, value: str,field_name:str=None) -> str:
        if value is None:
            return value
        self.field_name = field_name
        if self.inclusive is True:
            if value > self.comparable:
                raise ValidationError(self._format_error(value))
        else:
            if value >= self.comparable:
                raise ValidationError(self._format_error(value))

        return value