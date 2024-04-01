# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-import

from dataclasses import dataclass
import re
from typing import Iterable, OrderedDict, Sized, Union
from collections import OrderedDict
import volent.settings.types as _t
import colemen_utils as c

# @dataclass
# class Trigger:
#     model:_t.model_type = None
#     when:str = None

#     def __init__(
#         self,
#         model:_t.model_type,
#         when:str,
#         ):
#         self.model = model
#         self.when = when




#     @property
#     def create_statement(self):
#         '''
#             Get this Trigger's create_statement

#             `default`:None


#             Meta
#             ----------
#             `@author`: Colemen Atwood
#             `@created`: 05-08-2023 11:28:54
#             `@memberOf`: Trigger
#             `@property`: create_statement
#         '''
#         value = self.create_statement
#         if value is None:
#             value = somethingGoesHere
#             self.create_statement = value
#         return value
    

