# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-import
'''
    The query delete module.

    ----------

    Meta
    ----------
    `author`: Colemen Atwood
    `created`: 04-28-2023 07:24:17
    `name`: delete
    * @xxx [04-28-2023 07:24:33]: documentation for delete
'''



from dataclasses import dataclass
from typing import Iterable, Union


import colemen_utils as c


import volent.settings.types as _t
import volent.settings as _settings
# from volent.Field import Field as _field
# from volent.Relationship import Relationship as _relationship
# from volent.UniqueConstraint import UniqueConstraint as _uniqueConstraint


@dataclass
class QueryParam:
    Query:_t.query_type = None
    name:str = None
    value:any = None

    def __init__(self,Query:_t.query_type,name:str,value) -> None:
        self.Query = Query
        self.name = name
        self.value = value

    def __repr__(self) -> str:
        return f"<QueryParam : {self.name} :: {self.value}>"

    def serialize(self)->dict:
        '''Get this param as a dictionary.'''
        return {self.name:self.value}

    @property
    def parameterized_name(self)->str:
        '''Generate the parameterized name of this param.

        Example:
        - @title : when sqlite is being used.'''
        if _settings.globe.flavor in ["sqlite"]:
            return f"@{self.name}"
        else:
            return f":{self.name}"
    # parameterized_name = paramaterized_name

    @property
    def parameterized_update_string(self)->str:
        '''Generate the placeholder string used for this parameter when updating a column.

        Example:
        - track_number = @track_number
        '''
        if _settings.globe.flavor in ["sqlite"]:
            return f"{self.name}=@{self.name}"
        else:
            return f"{self.name}=:{self.name}"

