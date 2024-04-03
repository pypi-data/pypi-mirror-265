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


import volent.settings as _settings
import volent.settings.types as _t
# import volent.settings as _settings
# from volent.Field import Field as _field
# from volent.Relationship import Relationship as _relationship
# from volent.UniqueConstraint import UniqueConstraint as _uniqueConstraint


@dataclass
class WhereClause:
    Query:_t.query_type = None
    column_name:str = None
    value:any = None
    max_value:any = None
    comparison:str = None
    # comparison_operator:str = None
    is_or_parent:bool = False
    or_parent_id:str = None
    or_child_count:int = 0
    is_or_child:bool = False


    def __init__(self,Query:_t.query_type,column_name:str,value,comparison:str) -> None:
        '''
            Create a delete query instance.

            ----------

            Arguments
            -------------------------
            `model` {model}
                The model instance to execute a delete operation on.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 04-28-2023 07:24:53
            `memberOf`: Delete
            `version`: 1.0
            `method_name`: Delete
            * @xxx [04-28-2023 07:26:55]: documentation for Delete
        '''
        self.Query = Query
        self._params = {}
        self.column_name = column_name
        self.comparison = comparison

        self.value = value or "NULL"
        snake_comp = c.string.to_snake_case(comparison)


        if snake_comp == "or":
            self.comparison = "or"
            self.is_or_parent = True
            self.or_parent_id = c.rand.css_class()


        if snake_comp in ["!","!=","isnt","isnot","is_not","<>"]:
            self.comparison = "is not"

        # if snake_comp in ["greater_than"]:
        #     self.comparison = ">"

        # if snake_comp in ["greater_than_equal"]:
        #     self.comparison = ">="

        if snake_comp in ["in","not_in"]:
            self.value = c.arr.force_list(self.value)


        if snake_comp == "between":
            self.value = value[0]
            self.max_value = value[1]

        if snake_comp == "in":
            self.value = c.arr.force_list(value)


    def __repr__(self) -> str:
        if self.is_or_parent:
            return f"<WhereClause OR: {self.or_parent_id} :: {self.or_child_count}>"
        return f"<WhereClause : {self.column_name} :: {self.comparison} :: {self.value} :: {self.or_parent_id}>"

    def set_or_id(self,or_id):
        print(self)
        print(f"set or id: {or_id}")
        self.or_parent_id = or_id
        print(self)

    @property
    def comparison_operator(self):
        '''
            Get this WhereClause's comparison_operator

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 04-01-2024 16:18:47
            `@memberOf`: WhereClause
            `@property`: comparison_operator
        '''

        snake_comp = c.string.to_snake_case(self.comparison)
        match snake_comp:
            case "greater_than":
                return ">"
            case "greater_than_equal":
                return ">="
            case "less_than":
                return "<"
            case "less_than_equal":
                return "<="
        if self.comparison in [">","<","=","!=",">=","<="]:
            return self.comparison
        return self.comparison.upper()



    def where_string(self):
        '''Generate the SQL for this where clause'''
        snake_comp = c.string.to_snake_case(self.comparison)
        # if self.is_or_parent is True:

        if snake_comp in ["or"]:
            subwheres = []
            children = self.Query.get_wheres_by_or_id(self.or_parent_id)
            # print(f"whereClause.where_string : or child count : {len(children)}")
            for ch in children:
                cws = ch.where_string()
                # print(f"cws: {cws}")
                subwheres.append(cws)
            sub_string = ' OR '.join(subwheres)
            if self.Query.where_count > 0:
                sub_string = f"({sub_string})"
            return sub_string



        if snake_comp in ["is_not"]:
            if self.value != "NULL":
                return f"{self.column_name} != {self.quoted_value}"


        if snake_comp in ["is","is_not"]:
            comp = self.comparison.upper()
            p = self.Query.add_param(c.rand.css_class(),self.value)
            if self.should_quote:
                comp = "!="
                if snake_comp == "is":
                    comp = "="
            return f"{self.column_name} {comp} {p.parameterized_name}"

        if snake_comp in ["greater_than","greater_than_equal","less_than","less_than_equal"]:
            p = self.Query.add_param(c.rand.css_class(),self.value)
            return f"{self.column_name} {self.comparison_operator} {p.parameterized_name}"

        if snake_comp in ["between"]:
            min_key = c.rand.rand()
            max_key = c.rand.rand()
            min_param = self.Query.add_param(min_key,self.value)
            max_param = self.Query.add_param(max_key,self.max_value)
            # min_key =f"{wcol}_minimum"
            # max_key =f"{wcol}_maximum"

            return f"{self.column_name} {self.comparison.upper()} {min_param.parameterized_name} AND {max_param.parameterized_name}"


        if snake_comp in ["between"]:
            return f"{self.column_name} {self.comparison.upper()} {self.quoted_value}"


        if snake_comp in ["in","not_in"]:
            inlist = []
            for v in self.value:
                key = c.rand.rand()
                if _settings.globe.flavor in ['sqlite']:
                    inlist.append(f"@{key}")
                    self.Query.add_param(key,v)
            inlist_string = ','.join(inlist)
            return f"{self.column_name} {self.comparison.upper()} ({inlist_string})"


        if snake_comp in ["like"]:
            # p = self.Query.add_param(c.rand.css_class(),self.value)
            # return f"{self.column_name} {self.comparison.upper()} '{p.parameterized_name}'"
            return f"{self.column_name} {self.comparison.upper()} '{self.value}'"



    @property
    def quoted_value(self):
        '''
            returns the value wrapped in quotes IF the column's python data type is string.
        '''
        if self.should_quote:
            return f"'{self.value}'"
        return self.value


    @property
    def should_quote(self):
        '''
            True if the column's python data type is a string.
        '''
        col = self.Query.model.get_column(self.column_name)
        # print(f"col.data_type : {col.data_type}")
        if self.value == "NULL":
            return False
        if isinstance(self.value,col.data_type.python_data_type):
            return True
        return False







