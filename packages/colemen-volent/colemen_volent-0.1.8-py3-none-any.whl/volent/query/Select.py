# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-import


from dataclasses import dataclass
import re
from typing import Iterable,OrderedDict, Union


import colemen_utils as c


import volent.settings.types as _t
import volent.settings as _settings
from volent.Field import Field as _field
# from volent.Relationship import Relationship as _relationship
# from volent.UniqueConstraint import UniqueConstraint as _uniqueConstraint
from volent.query.Query import Query
from volent.query.WhereMixin import WhereMixin
from mysql.connector.errors import OperationalError,InterfaceError

@dataclass
class Select(Query,WhereMixin):
    def __init__(self,model:_t.model_type,columns=None,limit:int=100,offset:int=0) -> None:
        self._params = {}
        self._selects = []
        self._joins = []
        # self._limit = limit
        # self._offset = offset

        self.query_crud_type = "read"
        if columns is None:
            columns = model.columns
        if isinstance(columns,(tuple)):
            if len(columns) == 1:
                columns = columns[0]
        # print(f"Select.__init__.columns : {columns}")
        super().__init__(model,select_columns=columns)

    @property
    def has_joins(self):
        '''
            Get this Select's has_joins

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 05-07-2023 16:56:27
            `@memberOf`: Select
            `@property`: has_joins
        '''
        if len(self._joins) > 0:
            return True
        return False

    @property
    def select_string(self)->str:
        '''
            Get the compiled select string for this query.

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 12-09-2022 15:56:15
            `@memberOf`: SelectQuery
            `@property`: select_string
        '''
        if len(self._selects) == 0:
            value = "*"
        else:
            selects = []
            for sel in self._selects:
                value = None
                if sel['alias'] is not None:
                    value = f"{sel['column_name']} as {sel['alias']}"
                else:
                    value = f"{sel['column_name']}"
                if value is not None:
                    selects.append(value)
            value = ', '.join(selects)

        if self._count is True:
            value = f"COUNT({value})"
        if self._average is True:
            value = f"AVG({value})"
        if self.sum_ is True:
            value = f"SUM({value})"
        return value


    @property
    def query(self):

        # print(f"self.select_string: {self.select_string}")

        value = f"""SELECT {self.select_string} FROM {self.model.quoted_name}{self.left_join_string}{self.where_string}"""

        # value = self._paginate_select_query(value)
        # value = self._format_query_params(value,self._params)
        # print(f"value: {value}")
        # print(f"self._params: {self._params}")
        return value,self.serialized_params

    def execute(self,return_models=True)->Union[bool,dict,int,_t.model_type]:
        '''
            Execute the select query on the table.

            ----------

            Arguments
            -------------------------
            [`return_models`=True] {bool}
                If False, this will return a dictionry or list of dictionaries.


            Return {bool,dict,list,int,model}
            ----------------------
            returns False if the query is malformed or could not be executed.
            The results of the query otherwise.

            If return_models is True, it will generate a new model instance for each row.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 04-28-2023 07:54:49
            `memberOf`: Select
            `version`: 1.0
            `method_name`: execute
            * @xxx [04-28-2023 07:57:23]: documentation for execute
        '''
    # def execute(self)->Union[bool,dict,int]:
        # _mysql_connector.MySQLInterfaceError: Lost connection to MySQL server during query
        sql,args= self.query

        if sql is False:
            return False

        # print(f"sql:{sql}")
        # print(f"args:{args}")
        try:
            # @Mstep [] execute the insert query.

            # result = self.database.run_select(sql,args)
            result = self.database.run_select_internal(sql,self,args)

            # print(f"result : {type(result)} : {result}")
            if return_models and result is not None:
                models = []
                # if isinstance(result[0],(tuple)) is False:
                #     result = [result]
                for r in result:
                    # print(f"r : {r}")
                    mdl = self.model.__class__(**r)
                    mdl.__doc__ = self.model.__doc__
                    mdl._model_name = self.model._model_name
                    mdl._database_name = self.model._database_name
                    mdl._database = self.model._database
                    models.append(mdl)
                return models
        except OperationalError as e:
            c.con.log(e,"red")
        except InterfaceError as e:
            c.con.log(e,"red")
        return result

    def count(self)->_t.query_type:
        '''
            Count the number of rows that are selected.

            ----------


            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 04-28-2023 07:57:50
            `memberOf`: Select
            `version`: 1.0
            `method_name`: count
            * @xxx [04-28-2023 07:58:26]: documentation for count
        '''
        self._count = True
        return self

    def average(self)->_t.query_type:
        '''
            Calculate the average of all the rows that are selected.

            ----------


            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 04-28-2023 07:58:34
            `memberOf`: Select
            `version`: 1.0
            `method_name`: average
            * @xxx [04-28-2023 07:59:02]: documentation for average
        '''
        self._average = True
        return self

    def sum_(self)->_t.query_type:
        '''
            Calculate the sum of all the rows that are selected.

            ----------

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 04-28-2023 07:59:07
            `memberOf`: Select
            `version`: 1.0
            `method_name`: sum_
            * @xxx [04-28-2023 07:59:29]: documentation for sum_
        '''
        self._sum = True
        return self

    def add_select(self,column_name,alias=None)->_t.query_type:
        '''
            Add a column to the selection of this query.

            By default "*" is used to select all columns if None are specified.
            ----------

            Arguments
            -------------------------
            `column_name` {str}
                The name of the column to select
            [`alias`=None] {str}
                An alias to use for this column

            Return {None}
            ----------------------
            returns nothing

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 12-13-2022 12:04:31
            `memberOf`: SelectQuery
            `version`: 1.0
            `method_name`: add_select
            * @xxx [12-13-2022 12:06:00]: documentation for add_select
        '''
        if self.model is not None:
            if self.model.get_column(column_name) is None:
                c.con.log(f"Column {column_name} does not exist in table: {self.model.name}","warning")
                return
        data = {
            "column_name":column_name,
            "alias":alias,
        }
        self._selects.append(data)
        return self

    def left_join(self,model:_t.model_type,column_name:str):
        data = {
            "join_type":"LEFT",
            "model":model,
            "table_name":model.quoted_name,
            "column_name":column_name,
        }
        self._joins.append(data)
    # def left_join(self,table_name:str,column_name:str):
    #     data = {
    #         "join_type":"LEFT",
    #         "table_name":table_name,
    #         "column_name":column_name,
    #     }
    #     self._joins.append(data)


    @property
    def left_join_string(self):
        '''
            Get this Select's left_join_string

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 04-21-2023 08:58:54
            `@memberOf`: Select
            `@property`: left_join_string
        '''
        out_list = []
        for join in self._joins:
            if join['join_type'] != "LEFT":
                continue
            template = f""" {join['join_type']} JOIN {self.model.quoted_name}
    ON {self.model.quoted_name}.{join['column_name']} = {join['table_name']}.{join['column_name']}"""
            return template
        return ""


    def paginate(self,page_number:int=1,per_page:int=None):
        '''
            update the pagination settings for this query.

            Arguments
            -------------------------
            `page_number` {int} = 1
                Which page of items to return

                If set to 0, None or False the query will NOT be paginated.

            `per_page` {int} = None
                How many items per page should be shown.

            Return {Select}
            ----------------------
            returns this select instance.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 04-02-2024 10:14:25
            `memberOf`: Select
            `version`: 1.0
            `method_name`: paginate
            * @xxx [04-02-2024 10:16:07]: documentation for paginate
        '''
        self._page_number = page_number
        if per_page is not None:
            self._items_per_page = per_page
        return self

    def _paginate_query(self,sql:str)->str:
        page_number = self._page_number
        per_page = self._items_per_page
        offset = None if (page_number * per_page) < 1 else page_number * per_page
        limit = per_page

        if limit in [0,None,False]:
            return sql

        # @Mstep [] remove any trailing spaces and semicolons
        sql = c.string.strip(sql,[";"," "],"right")
        # @Mstep [] remove any already existing pagination strings.
        sql = re.sub(r'limit\s*[0-9]*\s*(,|offset)\s*(:?[0-9\s]*)?',"",sql,re.MULTILINE | re.IGNORECASE)

        limit_string = f"LIMIT {limit}"
        offset_string = ""
        if offset is not None:
            offset_string = f"OFFSET {offset}"

        paginate = f"{limit_string} {offset_string}"
        sql = f"{sql} {paginate}"
        return sql


    def __repr__(self) -> str:
        return f"<Select : {self.model.model_name}>"


def format_null(value):
    if value is None:
        return "NULL"
    return value

