import urllib
from sqlalchemy import create_engine,text
from sqlalchemy.engine import Result
from typing import Optional,List,Tuple,Any
from config import DB_TYPE,MSSQL_DEFAULT_PORT,ORACLE_DEFAULT_PORT,INVALID_PORT

type DatabaseResult = List[Tuple[Any,...]]

def get_connection_string(host:str,\
                          database_name:str,\
                          user:str,\
                          password:str,\
                          port:int=INVALID_PORT,\
                          is_sid:bool=False)->Optional[str]:
    
    connection_string = None
    
    if DB_TYPE=="mssql":
        
        driver = "{ODBC Driver 17 for SQL Server}"

        if port==INVALID_PORT:
            port = MSSQL_DEFAULT_PORT

        odbc_str = f"DRIVER={driver};SERVER={host};PORT={port};UID={user};DATABASE={database_name};PWD={password}"

        connection_string = f"mssql+pyodbc:///?odbc_connect={urllib.parse.quote_plus(odbc_str)}"

    elif DB_TYPE=="oracle":
        
        if port==INVALID_PORT:
            port = ORACLE_DEFAULT_PORT

        user = urllib.parse.quote_plus(user)

        password = urllib.parse.quote_plus(password)

        if is_sid:
            connection_string = f"oracle+oracledb://{user}:{password}@{host}:{port}/?sid={database_name}"
        else:
            connection_string = f"oracle+oracledb://{user}:{password}@{host}:{port}/?service_name={database_name}"
 

    return connection_string

def test_connection(connection_str:str)->bool:
    """
    Test whether we can connect to database
    """
    try:
        engine = create_engine(connection_str)

        with engine.connect() as connection:
            return True
    except:
        return False
    
def query(connection_str:str,query:str)->Optional[DatabaseResult]:
    
    try:
        engine = create_engine(connection_str)

        with engine.connect() as connection:
            result = connection.execute(text(query))

            return [tuple(row) for row in result]
    except:
        return None