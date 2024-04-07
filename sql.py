from typing import Any
import sqlite3, mysql.connector, os


class local_sqlite3:
    """create a local db file with lower and easy code
    
    ---
    # create_table_if_not()
    #### CREATE TABLE IF NOT EXISTS `table`
        ```python
        from TOOLS.sql import local_sql()
        
        db = local_sql("path/to/file.db")
        db.create_table_if_not(
            table= "table name", 
            content= {
                "id": "INTEGER",
                "first name": "TEXT",
            }
        )
        ```
        
    ---
    # insert_into_db()
    #### INSERT INTO `table` VALUES (`content`)
        ```python
        from TOOLS.sql import local_sql
        db = local_sql("path/to/file.db")
        db.insert_into_db(
            table="table",
            content= {
                "first name" :'NooR',
                "last name" :"MaseR",
                "country" :'EGYPT'
            }
        )
        ```
        
    ---
    # find_into_db()
    #### SELECT * FROM `table` `where`
        ```python
        from TOOLS.sql import local_sql
        db = local_sql("path/to/file.db")
        
        # like=False meens first name = "NOOR"
        data1 = db.find_into_db(
            table="table",
            where= {
                "first name": "NooR"
            },
            like=False,
        )
        print(data1)
        
        # like=True meens first name like "NOOR"
        data2 = db.find_into_db(
            table="table",
            where= {
                "first name": "NooR"
            },
            like=True
        )
        print(data2)
        ```
        
    ---
    # find_cols_into_db()
    #### SELECT `column_name` FROM `table` `where`
        ```python
        from TOOLS.sql import local_sql
        db = local_sql("path/to/file.db")
        
        # like=False meens first name = "NOOR"
        data1 = db.find_cols_into_db(
            table="table",
            column_name="owner",
            where= {
                "first name": 'NOOR'
            },
            like= False
        )
        print(data1)
        
        # like=True meens first name like "NOOR"
        data2 = db.find_cols_into_db(
            table="table",
            column_name="owner",
            where= {
                "first name": 'NOOR'
            },
            like= True
        )
        print(data2)
        ```
        
    ---
    # Get_db_data()
    #### SELECT * FROM `table`
        ```python
        from TOOLS.sql import local_sql
        
        db = local_sql("path/to/file.db")
        print(db.Get_db_data(table="table"))
        ```
        
    ---
    # Update_db_data()
    #### Update `table` `set_command` `where`
        ```python
        from TOOLS.sql import local_sql
        
        db = local_sql("path/to/file.db")
        db.Update_db_data(
            table="table",
            set_command={"Salary": 5000},
            where={
                "email": "MaseR@example.org",
                "phone":"+20*********",
                "ID": "**********",
                "country": "EGYPT"
            },
            like= False
        ```
    ---
    # Delete_from_db()
    #### DELETE FROM `table` `where`
        ```python
        from TOOLS.sql import local_sql
        
        db = local_sql("path/to/file.db")
        db.Delete_from_db(
            table="table",
            where = {
                "EMAIL": "MaseR@example.org",
                "PASSWORD": "123456789",
                "PHONE": "+1*******")
            }
        ```
    ---
    # Execute()
    Execute an SQLite command By your own
    auto `commit()`
    """
    
    def __init__(self, db_filename: str) -> None:
        self._sql_command: str
        self.db_filename: str = db_filename
        
        if os.path.splitext(self.db_filename)[-1] != ".db":
            raise FileNotFoundError("the file is not a db file")
        if not os.path.exists(self.db_filename):
            with self.__connect():
                pass
        
    def __connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_filename)
    
    def create_table_if_not(self, table: str, content: dict[str, str]) -> None:
        """
        ### CREATE TABLE IF NOT EXISTS `table`
        ```python
        from TOOLS.sql import local_sql()
        
        db = local_sql("path/to/file.db")
        db.create_table_if_not(
            table= "table name", 
            content= {
                "id": "INTEGER",
                "first name": "TEXT",
            }
        )
        ```
        """
        if self.db_filename.endswith(".db"):
            creation: str = f"CREATE TABLE IF NOT EXISTS {table} ({', '.join([f"'{k}' {v.upper()}" for k,v in content.items()])})"
            self._sql_command = creation
            
            with self.__connect() as conn:
                c = conn.cursor()
                c.execute(self._sql_command)
                conn.commit()
                c.close()
        else:
            raise FileNotFoundError(f"the [{self.db_filename}] does not appere to be a db file")
    
    def insert_into_db(self, table: str, content: dict[str, Any]) -> None:
        """
        ### INSERT INTO `table` VALUES (`content`)
        ```python
        from TOOLS.sql import local_sql
        db = local_sql("path/to/file.db")
        db.insert_into_db(
            table="table",
            content= {
                "first name" :'NooR',
                "last name" :"MaseR",
                "country" :'EGYPT'
            }
        )
        ```
        """
        if self.db_filename.endswith(".db"):
            insert: str = f"INSERT INTO '{table}' "
            keys = tuple(content.keys())
            values = tuple(content.values())
            with self.__connect() as connector:
                c = connector.cursor()
                unknown = f"({','.join(['?' for _ in keys])})"
                self._sql_command = f"{insert} {keys} VALUES {unknown}"
                c.execute(self._sql_command, values)
                connector.commit()
                c.close()
        else:
            raise FileNotFoundError(f"the [{self.db_filename}] does not appere to be a db file")

    def find_into_db(self, table: str, where: dict[str, Any], like:bool = False) -> list:
        """
        ### SELECT * FROM `table` `where`
        ```python
        from TOOLS.sql import local_sql
        db = local_sql("path/to/file.db")
        
        # like=False meens first name = "NOOR"
        data1 = db.find_into_db(
            table="table",
            where= {
                "first name": "NooR"
            },
            like=False,
        )
        print(data1)
        
        # like=True meens first name like "NOOR"
        data2 = db.find_into_db(
            table="table",
            where= {
                "first name": "NooR"
            },
            like=True
        )
        print(data2)
        """
        if self.db_filename.endswith(".db"):
            query: str = "AND ".join([f"`{k}` {"like" if like else '='} `{v}`" for k,v in where.items()])
            with self.__connect() as connect:
                c = connect.cursor()
                self._sql_command = f"SELECT * FROM '{table}' WHERE ({query})"
                c.execute(f"SELECT * FROM {table} {query}")
                result = c.fetchall()
                connect.commit()
                c.close()
            return result
        else:
            raise FileNotFoundError(f"the [{self.db_filename}] does not appere to be a db file")

    def find_cols_into_db(self, table: str, columns: tuple | list[str], where: dict[str, Any], like: bool = False) -> list:
        """
        ### SELECT `column_name` FROM `table` `where`
        ```python
        from TOOLS.sql import local_sql
        db = local_sql("path/to/file.db")
        
        # like=False meens first name = "NOOR"
        data1 = db.find_cols_into_db(
            table="table",
            column_name="owner",
            where= {
                "first name": 'NOOR'
            },
            like= False
        )
        print(data1)
        
        # like=True meens first name like "NOOR"
        data2 = db.find_cols_into_db(
            table="table",
            column_name="owner",
            where= {
                "first name": 'NOOR'
            },
            like= True
        )
        print(data2)
        ```
        """
        if self.db_filename.endswith(".db"):
            condition = " AND ".join([f'{k} {"LIKE" if like else "="} "{v}"' for k, v in where.items()])
            cols = ", ".join([f"{col}" for col in columns])
            self._sql_command = f"SELECT {cols} FROM `{table}` WHERE {condition}"
            
            with self.__connect() as connect:
                c = connect.cursor()
                c.execute(self._sql_command)
                result = c.fetchall()
                connect.commit()
                c.close()
            return result
        else:
            raise FileNotFoundError(f"the [{self.db_filename}] does not appere to be a db file")

    def Get_db_data(self, table: str) -> list[Any]:
        """
        ### SELECT * FROM `table`
        ```python
        from TOOLS.sql import local_sql
        
        db = local_sql("path/to/file.db")
        print(db.Get_db_data(table="table"))
        ```
        """
        if self.db_filename.endswith(".db"):
            with self.__connect() as connect:
                c = connect.cursor()
                self._sql_command = f"""SELECT * FROM "{table}" """
                c.execute(self._sql_command)
                result = c.fetchall()
                connect.commit()
                c.close()
            return result
        else:
            raise FileNotFoundError(f"the [{self.db_filename}] does not appere to be a db file")

    def Update_db_data(self, table: str, set_command: dict[str, Any], where: dict[str, Any], like: bool = False) -> None:
        """
        ### Update `table` `set_command` `where`
        ```python
        from TOOLS.sql import local_sql
        
        db = local_sql("path/to/file.db")
        db.Update_db_data(
            table="table",
            set_command={"Salary": 5000},
            where={
                "email": "MaseR@example.org",
                "phone":"+20*********",
                "ID": "**********",
                "country": "EGYPT"
            },
            like= False
        ```
        """
        if self.db_filename.endswith(".db"):
            
            update = ", ".join([f'{k} = "{v}"' for k, v in set_command.items()])
            where_query = " AND ".join([f'{k} {"LIKE" if like else "="} "{v}"' for k, v in where.items()])
           
            with self.__connect() as connect:
                c = connect.cursor()
                self._sql_command = f"UPDATE '{table}' SET {update} WHERE {where_query}"
                c.execute(self._sql_command)
                connect.commit()
                c.close()
        else:
            raise FileNotFoundError(f"the [{self.db_filename}] does not appere to be a db file")

    def Delete_from_db(self, table: str, where: dict[str, Any], like: bool = False) -> None:
        """
        ### DELETE FROM `table` `where`
        ```python
        from TOOLS.sql import local_sql
        
        db = local_sql("path/to/file.db")
        db.Delete_from_db(
            table="table",
            where = {
                "EMAIL": "MaseR@example.org",
                "PASSWORD": "123456789",
                "PHONE": "+1*******")
            }
        ```
        """
        if self.db_filename.endswith(".db"):

            query = " AND ".join([f'{k} {"LIKE" if like else "="} "{v}"' for k, v in where.items()])
            
            with self.__connect() as connect:
                c = connect.cursor()
                self._sql_command = f"DELETE FROM `{table}` WHERE {query}"
                c.execute(str(self._sql_command))
                connect.commit()
                c.close()
        else:
            raise FileNotFoundError(f"the [{self.db_filename}] does not appere to be a db file")
        
    def Execute(self, exec: str) -> tuple[sqlite3.Connection, sqlite3.Cursor]:
        """
        Execute an SQLite3 command By your own
        
        auto `commit()`
        """
        conn = self.__connect()
        c = conn.cursor()
        c.execute(exec)
        conn.commit()
        return (conn, c)
        
class online_mysql:
    """an easy way to interact with mySQL with one line of code
    # set_database()
    set | connect to a database
    
    ---
    # create_table()
    ### CREATE TABLE IF NOT EXISTS `table`
    ```python
        from TOOLS.sql import online_mysql()
        
        db = lonline_mysql("path/to/file.db")
        db.create_table(
            table= "table name", 
            fields= {
                "id": "INTEGER",
                "first name": "TEXT",
            }
        )
        
    ```
    ---
    # insert_into_db()
    ### INSERT INTO `table` VALUES (`content`)
        ```python
        from TOOLS.sql import online_mysql
        db = online_mysql("path/to/file.db")
        db.insert_into_db(
            table="table",
            content= {
                "first_name" :'NooR',
                "last_name" :"MaseR",
                "country" :'EGYPT'
            }
        )
        ```
        
    ---
    # find_cols_into_db()
    ### SELECT `column_name` FROM `table` `where`
        ```python
        from TOOLS.sql import online_mysql
        db = online_mysql("path/to/file.db")
        
        # like=False meens first name = "NOOR"
        data1 = db.find_cols_into_db(
            table="table",
            colums=("owner", "number"),
            where= {
                "first name": 'NOOR'
            },
            like= False
        )
        print(data1)
        
        # like=True meens first name like "NOOR"
        data2 = db.find_cols_into_db(
            table="table",
            column_name=("owner", "number"),
            where= {
                "first name": 'NOOR'
            },
            like= True
        )
        print(data2)
        ```
    ---
    # Get_db_data()
    ### SELECT * FROM `table`
        ```python
        from TOOLS.sql import online_mysql
        
        db = online_mysql("path/to/file.db")
        print(db.Get_db_data(table="table"))
        ```
    ---
    # Update_db_data()
    ### Update `table` `set_command` `where`
        ```python
        from TOOLS.sql import online_mysql
        
        db = online_mysql("path/to/file.db")
        db.Update_db_data(
            table="table",
            set_command={"Salary": 5000},
            where={
                "email": "MaseR@example.org",
                "phone":"+20*********",
                "ID": "**********",
                "country": "EGYPT"
            },
            like= False
        ```
    ---
    # Delete_from_db()
    ### DELETE FROM `table` `where`
        ```python
        from TOOLS.sql import online_mysql
        
        db = online_mysql("path/to/file.db")
        db.Delete_from_db(
            table="table",
            where = {
                "EMAIL": "MaseR@example.org",
                "PASSWORD": "123456789",
                "PHONE": "+1*******")
            },
            like= False
        ```
    ---
    # Execute()
    create your own MySql Command
    """
    def __init__(self, host: str = "localhost", user: str = "root", password: str = "123", database: str | None = None) -> None:
        self.__host: str = host
        self.__user: str = user
        self.__password: str = password
        self.__database: str | None = database
        self._sql_command: str
        
    def __connect(self):
        return mysql.connector.connect(
            host= self.__host,
            user= self.__user,
            password= self.__password,
            database = self.__database
        )
    
    def set_database(self, database: str) -> None:
        self.__database = database
        
    def create_table(self, table: str, fields: dict[str, str], do_if_not_exist: bool = True) -> None:
        """
        ### CREATE TABLE IF NOT EXISTS `table`
        ```python
        from TOOLS.sql import online_mysql()
        
        db = lonline_mysql("path/to/file.db")
        db.create_table(
            table= "table name", 
            fields= {
                "id": "INTEGER",
                "first name": "TEXT",
            }
        )
        ```
        """
        columns = ", ".join([f"{name} {type.upper()}" for name, type in fields.items()])
        creation_query = f"CREATE TABLE {"IF NOT EXISTS" if do_if_not_exist else ""} {table} ({columns})"

        with self.__connect() as conn:
            with conn.cursor() as c:
                c.execute(creation_query)
                self._sql_command = creation_query
    
    def insert_into_db(self, table: str, content: dict[str, Any]) -> None:
        """
        ### INSERT INTO `table` VALUES (`content`)
        ```python
        from TOOLS.sql import online_mysql
        db = online_mysql("path/to/file.db")
        db.insert_into_db(
            table="table",
            content= {
                "first_name" :'NooR',
                "last_name" :"MaseR",
                "country" :'EGYPT'
            }
        )
        ```
        """
    
        insert: str = f"INSERT INTO {table} "
        keys = tuple(content.keys())
        values = tuple(content.values())
        placeholders = ", ".join(["%s"] * len(keys))
        columns = ", ".join(keys)
        
        with self.__connect() as connector:
            c = connector.cursor()
            self._sql_command = f"{insert} ({columns}) VALUES ({placeholders})"
            c.execute(self._sql_command, values)
            connector.commit()
            c.close()

    def find_into_db(self, table: str, where: dict[str, Any], like:bool = False) -> list:
        """
        ### SELECT * FROM `table` `where`
        ```python
        from TOOLS.sql import local_sql
        db = local_sql("path/to/file.db")
        
        # like=False meens first name = "NOOR"
        data1 = db.find_into_db(
            table="table",
            where= {
                "first name": "NooR"
            },
            like=False,
        )
        print(data1)
        
        # like=True meens first name like "NOOR"
        data2 = db.find_into_db(
            table="table",
            where= {
                "first name": "NooR"
            },
            like=True
        )
        print(data2)
        """
            
        query: str = " AND ".join([f"`{k}` {"like" if like else '='} '{v}'" for k,v in where.items()])
        with self.__connect() as connect:
            with connect.cursor() as c:
                self._sql_command = f"SELECT * FROM `{table}` WHERE {query}"
                print(self._sql_command)
                c.execute(self._sql_command)
                result = c.fetchall()
        return result

    def find_cols_into_db(self, table: str, columns: list[str] | tuple, where: dict[str, Any], like: bool = False) -> list:
        """
        ### SELECT `column_name` FROM `table` `where`
        ```python
        from TOOLS.sql import online_mysql
        db = online_mysql("path/to/file.db")
        
        # like=False meens first name = "NOOR"
        data1 = db.find_cols_into_db(
            table="table",
            colums=("owner", "number"),
            where= {
                "first name": 'NOOR'
            },
            like= False
        )
        print(data1)
        
        # like=True meens first name like "NOOR"
        data2 = db.find_cols_into_db(
            table="table",
            column_name=("owner", "number"),
            where= {
                "first name": 'NOOR'
            },
            like= True
        )
        print(data2)
        ```
        """
        
        condition = " AND ".join([f'{k} {"LIKE" if like else "="} "{v}"' for k, v in where.items()])
        cols = ", ".join([f"{col}" for col in columns])
        self._sql_command = f"SELECT {cols} FROM `{table}` WHERE {condition}"

        with self.__connect() as connect:
            with connect.cursor() as c:
                c.execute(self._sql_command)
                result = c.fetchall()
        return result
    
    def Get_db_data(self, table: str) -> list[Any]:
        """
        ### SELECT * FROM `table`
        ```python
        from TOOLS.sql import online_mysql
        
        db = online_mysql("path/to/file.db")
        print(db.Get_db_data(table="table"))
        ```
        """
        
        with self.__connect() as connect:
            with connect.cursor() as c:
                self._sql_command = f"SELECT * FROM `{table}`"
                c.execute(self._sql_command)
                result = c.fetchall()
        return result

    def Update_db_data(self, table: str, set_command: dict[str, Any], where: dict[str, Any], like: bool = False) -> None:
        """
        ### Update `table` `set_command` `where`
        ```python
        from TOOLS.sql import online_mysql
        
        db = online_mysql("path/to/file.db")
        db.Update_db_data(
            table="table",
            set_command={"Salary": 5000},
            where={
                "email": "MaseR@example.org",
                "phone":"+20*********",
                "ID": "**********",
                "country": "EGYPT"
            },
            like= False
        ```
        """
        where_query:str = "WHERE "
        set_update:str = "SET  "
        set_update += ", ".join([f"`{k}` = '{v}'" for k,v in set_command.items()])      
        where_query += " AND ".join([f"`{k}` like '{v}'" for k,v in where.items()])
        
        with self.__connect() as connect:
            with connect.cursor() as c:
                self._sql_command = fr"""UPDATE `{table}` {set_update} {where_query}"""
                c.execute(self._sql_command)
                connect.commit()
    
    def Delete_from_db(self, table: str, where: dict[str, Any], like: bool = False) -> None:
        """
        ### DELETE FROM `table` `where`
        ```python
        from TOOLS.sql import online_mysql
        
        db = online_mysql("path/to/file.db")
        db.Delete_from_db(
            table="table",
            where = {
                "EMAIL": "MaseR@example.org",
                "PASSWORD": "123456789",
                "PHONE": "+1*******")
            },
            like= False
        ```
        """
        query:str = "WHERE "
        if like:
            query += " AND ".join([f"`{k}` like '{v}'" for k,v in where.items()])
        else:
            query += " AND ".join([f"`{k}` = '{v}'" for k,v in where.items()])

        with self.__connect() as connect:
            with connect.cursor() as c:
                self._sql_command = f"DELETE FROM `{table}` {query}"
                c.execute(self._sql_command)
                connect.commit()
    
    def Execute(self, query: str) -> list[Any]:
        "create your own MySql Command"
        with self.__connect() as connector:
            with connector.cursor() as c:
                c.execute(query)
                connector.commit()
                result = c.fetchall()
        return result
