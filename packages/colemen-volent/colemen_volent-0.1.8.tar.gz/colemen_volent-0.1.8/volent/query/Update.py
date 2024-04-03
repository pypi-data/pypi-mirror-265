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


@dataclass
class Update(Query,WhereMixin):
    def __init__(self,model:_t.model_type,columns=None) -> None:
        self._params = {}
        self._updates = []

        self.data = columns
        self.ignore_on_updates = False

        self.limit = 1
        '''Limit the number of rows that can be updated by this query.

        if set to 0, None or False, no limit will be applied.
        '''

        self.query_crud_type = "update"
        super().__init__(model,update_columns=columns)

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
        '''
            Generate the query string for this update.

            Return {tuple}
            ----------------------
            A tuple containing the query string and a dictionary of parameters

            If no parameters are used, its just an empty dict.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 04-02-2024 09:50:49
            `memberOf`: Update
            `version`: 1.0
            `method_name`: query
            * @xxx [04-02-2024 09:51:49]: documentation for query
        '''
        # print(self.data)
        self.updates_from_data()

        value = f"UPDATE {self.model.quoted_name} SET {self.update_string}{self.where_string}"

        value = self._paginate_query(value)
        # value = self._format_query_params(value,self._params)
        return value,self.serialized_params
        # return value,self._params

    def execute(
        self,
        foreign_key_checks:bool=True
        )->Union[bool,dict,int]:
        '''
            Execute this update operation on the model.

            ----------

            Arguments
            -------------------------

            [`foreign_key_checks`=True] {bool}
                If False, the query will not perform foreign key checks before executing the update.
                Be careful, this can cause integrity issues and will NOT warn you about it.


            Return {type}
            ----------------------
            return_description

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 04-28-2023 08:01:22
            `memberOf`: Update
            `version`: 1.0
            `method_name`: execute
            * @TODO []: documentation for execute
        '''
        sql,args= self.query

        if sql is False:
            return False

        # print(f"sql:{sql}")
        # print(f"args:{args}")

        # @Mstep [] execute the update query.
        result = self.database.run(sql,args,foreign_key_checks=foreign_key_checks)
        # @Mstep [] select the updated row as a dictionary.
        data = self.model.select().copy_wheres(self).execute(return_models=False)
        data = data[0]
        # @Mstep [LOOP] iterate the dictionary.
        for k,v in data.items():
            # @Mstep [] retrieve the column with a matching name from the model.
            col = self.model.get_column(k)
            col.value = v
            self.model._saved = True
        return data
        models = []
        for r in result:
            mdl = self.model.__class__(**r)
            mdl.__doc__ = self.model.__doc__
            mdl._name = self.model.name
            mdl._database_name = self.model._database_name
            mdl._database = self.model._database
            models.append(mdl)
        return models
        return result

    def updates_from_data(self)->dict:
        '''
        Parse this query's data to prepare it for updating the database.

        This will:
        - filter by existing columns
        - remove undefined values
        - apply on_update values

        returns a dictionary and sets the self._updates value.
        '''
        if self.data is None:
            self.data = self.model.data

        data = self.filter_dict_by_columns(self.data)
        updates = self.filter_undefined_values(data)

        if self.ignore_on_updates is False:
            updates = self.set_on_update_values(updates)
        self._updates = updates

        return updates



    @property
    def update_string(self):
        '''
            generate a string of placeholder values that will update columns.

            `example`: track_number=@track_number, genre=@genre

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 12-09-2022 15:56:15
            `@memberOf`: UpdateQuery
            `@property`: update_string
        '''
        if len(self._updates) == 0:
            return None
        else:
            placeholders = []
            for k,v in self._updates.items():
                p = self.add_param(k,v)
                placeholders.append(p.parameterized_update_string)
            value = ', '.join(placeholders)
        return value


    def add_update(self,column_name:str,value)->_t.update_query_type:
        '''
            add a column and its value to be updated with.

            Arguments
            -------------------------
            `column_name` {str}
                The name of the column to update

            `value` {any}
                The value to update the column with.

            Return {Update}
            ----------------------
            returns this query instance.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 04-02-2024 10:27:40
            `memberOf`: Update
            `version`: 1.0
            `method_name`: add_update
            * @xxx [04-02-2024 10:28:42]: documentation for add_update
        '''
        if self.data is None:
            self.data = {}
        self.data[column_name] = value
        return self
        # self._updates[column_name] = value

    def __repr__(self) -> str:
        return f"<Update : {self.model.model_name}>"


    def paginate(self,limit:Union[int,bool,None]=1)->_t.update_query_type:
        '''
            Set the pagination limit for this query.


            `Remember`: by default SQLITE does not support limiting updates/deletes so this will have no effect.

            Arguments
            -------------------------
            `limit` {int,bool,None}
                The number of rows that this query is allowed to update.

                If the limit is set to 0, None or False, no pagination will be added.

            Return {Update}
            ----------------------
            returns this query instance.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 04-02-2024 10:25:38
            `memberOf`: Update
            `version`: 1.0
            `method_name`: paginate
            * @xxx [04-02-2024 10:26:56]: documentation for paginate
        '''
        self.limit = limit
        return self


    def _paginate_query(self,sql:str)->str:
        '''
            Apply the pagination values to the query string.

            Because this is for an update query only the limit value is used.

            If the limit is set to 0, None or False, no pagination will be added.

            `Remember`: by default SQLITE does not support limiting updates/deletes so this will have no effect.

            Arguments
            -------------------------
            `sql` {string}
                The query string to apply pagination to.

            Return {str}
            ----------------------
            The sql with pagination added.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 04-02-2024 10:20:39
            `memberOf`: Update
            `version`: 1.0
            `method_name`: _paginate_query
            * @xxx [04-02-2024 10:25:28]: documentation for _paginate_query
        '''
        if _settings.globe.flavor in ["sqlite"]:
            return sql

        limit = self.limit
        offset = 0


        # @Mstep [] remove any trailing spaces and semicolons
        sql = c.string.strip(sql,[";"," "],"right")
        # @Mstep [] remove any already existing pagination strings.
        sql = re.sub(r'limit\s*[0-9]*\s*(,|offset)\s*(:?[0-9\s]*)?',"",sql,re.MULTILINE | re.IGNORECASE)

        if limit in [0,None,False]:
            return sql

        limit_string = f"LIMIT {limit}"
        offset_string = f"OFFSET {offset}"

        paginate = f"{limit_string} {offset_string}"
        paginate = f"{limit_string}"
        sql = f"{sql}\n {paginate}"
        return sql





def format_null(value):
    if value is None:
        return "NULL"
    return value

