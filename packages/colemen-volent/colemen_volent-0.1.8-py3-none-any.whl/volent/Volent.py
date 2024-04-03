# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-import
'''
    The main module of the volent library.

    ----------

    Meta
    ----------
    `author`: Colemen Atwood
    `created`: 04-28-2023 07:03:18
    `name`: volent
    * @xxx [04-28-2023 07:03:34]: documentation for volent
'''



import os
from typing import Iterable
import colemen_utils as c
import volent.settings as _settings
from volent.Model import Model as Model
from volent.Schema import Schema as Schema
from volent.Field import Field as Field
from volent.NestedField import NestedField as NestedField
from volent.Column import Column as Column
from volent.Relationship import Relationship as Relationship
from volent.UniqueConstraint import UniqueConstraint as UniqueConstraint
from volent.FullTextIndex import FullTextIndex as FullTextIndex
from volent.Database import Database as _Database
import volent.validate as validators
import volent.exceptions as exc
import volent.data_types as data_types
import volent.settings.types as _t
from volent.mixins.DatabaseConnection import DatabaseConnection as _DatabaseConnection
from volent.mixins.MySQLGeneratorMixin import MySQLGeneratorMixin as _MySQLGeneratorMixin
from volent.settings.types import no_default as noDefault
from volent.settings.types import undefined

class Volent(_DatabaseConnection,_MySQLGeneratorMixin):
    def __init__(
        self,
        index_existing_tables:bool=False
        ):
        self.models:Iterable[_t.model_type] = []
        '''A list of all registered model instances'''

        self.model_names:Iterable[str] = []
        '''A list of all registered model/table names'''

        self.unique_constraints:Iterable[_t.unique_constraint_type] = []
        '''A list of all registered unique constraint instances'''

        self.uq_names:Iterable[str] = []
        '''A list of all registered unique constraint names'''

        self.relationships:Iterable[_t.relationship_type] = []
        '''A list of all registered relationship instances'''

        self.relationship_names:Iterable[str] = []
        '''A list of all registered relationship names'''

        self.columns:Iterable[_t.column_type] = []
        '''A list of all registered column instances'''

        self._databases = []
        self.force_single_db = False

        self._index_existing_table:bool = index_existing_tables
        _settings.globe.Volent = self
        super().__init__()
        # self.set_defaults()

    # def set_defaults(self):
    #     self.settings = c.file.import_project_settings("volent.settings.json")

    def master(self):
        print("master")

    def summary(self,file_path:str=None)->dict:
        '''
            Generate a dictionary of summary data for all databases.

            ----------

            Arguments
            -------------------------
            [`file_path`=None] {str}
                The path to save the summary to, if not provided, it is saved to the working directory.

            Return {dict}
            ----------------------
            returns the summary dictionary

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 04-25-2023 08:05:45
            `memberOf`: Volent
            `version`: 1.0
            `method_name`: summary
            * @xxx [04-25-2023 08:26:06]: documentation for summary
        '''
        if file_path is None:
            file_path = f"{os.getcwd()}/summary.json"

        data = {
            "databases":[x.summary for x in self.databases]
        }
        c.file.writer.to_json(file_path,data)
        return data


    def start(self):
        '''
            Initiate the models, determine their relationships and connect to the databse.

            Raises a runtime error if it fails to connect to the database.

            ----------

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 04-25-2023 08:04:33
            `memberOf`: Volent
            `version`: 1.0
            `method_name`: start
            * @TODO []: documentation for start
        '''
        # self.models = []
        # self.model_names = []
        self.unique_constraints = []
        self.uq_names = []
        self.relationships = []
        self.relationship_names = []
        self.columns = []
        self._databases = []
        
        self._deep_registration()
        self._determine_relationships()
        self._generate_databases()
        # result = self.connect()
        if self.connect() is False:
            raise RuntimeError("Failed to connect to the database.")
        else:
            if self._index_existing_table is True:
                for db in self.databases:
                    db.existing_tables()


    def register(self,instance):
        '''
            Used internally for registration and mapping of the database structure.

            ----------

            Arguments
            -------------------------
            `instance` {any}
                The entity to register.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 04-25-2023 08:26:17
            `memberOf`: Volent
            `version`: 1.0
            `method_name`: register
            * @xxx [04-25-2023 08:26:56]: documentation for register
        '''
        if isinstance(instance,Model):
            # c.con.log(f"Registering New Model: {instance.name}","info")
            if instance.model_name in self.model_names:
                raise ValueError(f"Duplicate Name for Model : {instance.model_name}")
            if isinstance(self.force_single_db,(str)):
                instance._database_name = self.force_single_db
            self.models.append(instance)
            self.model_names.append(instance.model_name)


        if isinstance(instance,UniqueConstraint):
            # c.con.log(f"Register Unique Constraint: {instance.name}","info")
            if instance.name in self.uq_names:
                raise ValueError(f"Duplicate Name for Unique Constraint : {instance.name}")
            self.unique_constraints.append(instance)
            self.uq_names.append(instance.name)

        if isinstance(instance,Relationship):
            # c.con.log(f"Register Relationship: {instance.name}","info")
            self.relationships.append(instance)
            self.relationship_names.append(instance.name)

        if isinstance(instance,Column):
            # c.con.log(f"Register Column: {instance.name}","info")
            self.columns.append(instance)

    def get_column(self,name)->_t.column_type:
        '''
            Retrieve a column by its name.

            "database.table.column"

            ----------

            Arguments
            -------------------------
            `name` {str}
                The dot notation name.

                {database}.{table}.{column}

                {table}.{column}

            Return {column,None}
            ----------------------
            The column if it can be found, None otherwise

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 03-24-2023 08:30:03
            `memberOf`: BlackViper
            `version`: 1.0
            `method_name`: get_column
            * @xxx [03-24-2023 08:31:40]: documentation for get_column
        '''
        name = c.string.strip_excessive_chars(name,["."])
        nl = name.split(".")
        if len(nl) == 3:
            db_name = nl[0]
            mdl_name = nl[1]
            col_name = nl[2]
            db = self.get_database(db_name)
            if db is None:
                raise ValueError(f"Failed to locate column from {name}, Could not find database {db_name}")
            model = db.get_model(mdl_name)
            if model is None:
                raise ValueError(f"Failed to locate column from {name} - Could not find model {mdl_name}")
            column = model.get_column(col_name)
            if column is None:
                raise ValueError(f"Failed to locate column from {name} - Could not find column {col_name}")
            return column
        if len(nl) == 2:
            mdl_name = nl[0]
            col_name = nl[1]
            model = self.get_model(mdl_name)
            if model is None:
                raise ValueError(f"Failed to locate column from {name} - Could not find model {mdl_name}")
            column = model.get_column(col_name)
            if column is None:
                raise ValueError(f"Failed to locate column from {name} - Could not find column {col_name}")
            return column

    def get_model(self,name:str)->_t.model_type:
        '''
            Retrieve a model by searching for its name.

            ----------

            Arguments
            -------------------------
            `name` {str}
                The name of the model to search for.

                This can also be a dot path: database_name.table_name


            Return {model}
            ----------------------
            The model instance if successfull, None otherwise.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 04-25-2023 08:27:11
            `memberOf`: Volent
            `version`: 1.0
            `method_name`: get_model
            * @xxx [04-25-2023 08:28:14]: documentation for get_model
        '''
        name = c.string.strip_excessive_chars(name,["."])
        nl = name.split(".")
        if len(nl) == 2:
            name = nl[0]
        for md in self.models:
            if md.model_name == name:
                # print(f"---------------------------------name: {name}")
                return md

        return None

    # def get_base_model(self,)

    def _deep_registration(self):
        '''This will iterate all models to have their sub entities register with this instance.'''
        c.con.log("Initiating Deep Registration","info")
        for mdl in self.models:
            mdl.volent_register_subs()

    def _determine_relationships(self):
        c.con.log("Determining relationships between tables","info")

        # @Mstep [LOOP] iterate all relationship instances.
        # for rel in self.relationships:
        #     # @Mstep [] Attempt to retrieve the parent
        #     parent_string = rel.parent
        #     pm = self.get_model(parent_string)
        #     if pm is not None:
        #         print(f"    parent_string:{parent_string}")
        #         rel.parent_model = pm
        #     else:
        #         c.con.log(f"Failed to locate parent model for relationship {rel.name} from dot_path: {parent_string}","red")

        #     pc = self.get_column(parent_string)
        #     if pc is not None:
        #         rel.parent_column = pc



    @property
    def force_single_db(self):
        '''
            If this is a string, the __database_name__ of all models will be overridden to use that database.

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 05-08-2023 13:29:36
            `@memberOf`: Volent
            `@property`: force_single_db
        '''
        value = self._force_single_db
        return value
    
    @force_single_db.setter
    def force_single_db(self,value):
        '''
            Set the Volent's force_single_db property

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 05-08-2023 13:29:50
            `@memberOf`: Volent
            `@property`: force_single_db
        '''
        self._force_single_db = value
        # for m in self.models:
        #     m._database_name = value



    # ---------------------------------------------------------------------------- #
    #                                   DATABASES                                  #
    # ---------------------------------------------------------------------------- #

    @property
    def databases(self)->Iterable[_t.database_type]:
        '''
            Get a list of databases being managed by this instance.

            The result is None if there are no databases.

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 04-18-2023 08:16:56
            `@memberOf`: Volent
            `@property`: databases
        '''
        value = self._databases
        if len(value) == 0:
            value = None
        return value

    def _generate_databases(self):
        '''
            Locate all databases by iterating the models and create an instance for each unique name.


            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 04-18-2023 08:13:40
            `memberOf`: Volent
            `version`: 1.0
            `method_name`: _generate_databases
            * @xxx [04-18-2023 08:16:10]: documentation for _generate_databases
        '''
        self._databases = []
        names = self.get_databases_with_creds()
        if len(names) == 0:
            c.con.log("No Databases were specified in the models.","warning")
            return None

        for db in names:
            # @Mstep [] instantiate the database.
            dbi = _Database(self,db)
            # @Mstep [] have the database locate its associated tables.
            dbi.register_models()
            # @Mstep [] add the database instance to the databases list.
            self._databases.append(dbi)

    @property
    def database_names(self)->Iterable[str]:
        '''
            Get this Volent's database_names

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 04-17-2023 15:47:21
            `@memberOf`: Volent
            `@property`: database_names
        '''
        db_names = []
        for m in self.models:
            db_name = m.database_name
            if isinstance(db_name,(str)):
                if db_name not in db_names:
                    db_names.append(db_name)
        return db_names













    def generate_sql(self,file_path:str=None,drops:bool=True)->str:
        '''
            Generate the master SQL file for the database.

            ----------

            Arguments
            -------------------------
            [`file_path`=None] {str}
                The path to save the SQL to, it will default to the cwd/master.sql

            [`drops`=True] {bool}
                If False, it will not drop existing tables before creating them.

            Return {str}
            ----------------------
            The master SQL content as a string.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 04-25-2023 08:29:02
            `memberOf`: Volent
            `version`: 1.0
            `method_name`: generate_sql
            * @TODO []: documentation for generate_sql
        '''
        if file_path is None:
            file_path = f"{os.getcwd()}/master.sql"
        sql = self.master_sql(file_path,drops)
        return sql

    def clean_slate(self):
        '''If this is an sqlite database, this will delete the ENTIRE database.'''
        for db in self.databases:
            db.connection.close()
            file_name = f"{db.name}.db"
            print(f"file_name:{file_name}")
            c.file.delete(file_name)

        self.start()
        self.create_all()


    def drop_all_tables(self):
        '''
            Be Fucking careful.
            ----------

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 04-18-2023 09:40:21
            `memberOf`: Volent
            `version`: 1.0
            `method_name`: drop_all
            * @TODO []: documentation for drop_all
        '''
        # print(f"DROPPING ALL TABLES")
        for db in self.databases:
            # print(f"    db:{db.name}")
            db.drop_tables()
            db.drop_model_tables()

    def create_all(self,force=False):
        '''
            Create all schemas and tables in the database.
            
            ----------

            Arguments
            -------------------------
            [`force`=bool] {False}
                If True, this will drop the tables then recreate them

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 03-25-2023 10:57:44
            `memberOf`: BlackViper
            `version`: 1.0
            `method_name`: create_all
            * @TODO []: documentation for create_all
        '''

        # @Mstep [loop] iterate all registered databases
        if _settings.globe.flavor == "mysql":
            for db in self.databases:
                # @Mstep [IF] if force is True
                if force is True:
                    # @Mstep [] drop the database schema
                    db.run(db.drop_statement)
                # @Mstep [] create the database schema
                db.run(db.create_statement,foreign_key_checks=False)

                for mdl in db.models:
                    if force is True:
                        db.run(mdl.drop_statement)
                    db.run(mdl.create_statement,foreign_key_checks=False)
        if _settings.globe.flavor == "sqlite":
            for db in self.databases:

                for mdl in db.models:
                    # print(f"creating table: {mdl.model_name}")
                    if force is True:
                        db.run(mdl.drop_statement)
                    # print(mdl.create_statement)
                    db.run(mdl.create_statement,foreign_key_checks=False)
                    # print(f"\n\n")

if __name__ == '__main__':
    m = Volent()
    m.master()

