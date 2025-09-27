from model import Column,Dataset
from typing import List,Optional,Dict
from config import DB_TYPE,MSSQL_GET_INFO_SQL,ORACLE_GET_INFO_SQL
from database import query

def get_dataset(connection_str:str,\
                host:str,\
                database:str)->Optional[List[Dataset]]:

    if DB_TYPE=="mssql":
        return get_database_dataset(connection_str=connection_str,\
                                 host=host,\
                                database=database,\
                                query_info=MSSQL_GET_INFO_SQL)
    elif DB_TYPE=="oracle":
        return get_database_dataset(connection_str=connection_str,\
                                    host=host,\
                                    database=database,\
                                    query_info=ORACLE_GET_INFO_SQL)

    return None
    
def get_database_dataset(connection_str:str,\
                      host:str,\
                      database:str,\
                      query_info:str)->Optional[List[Dataset]]:
    
    grouped_column:Dict[str,List[Column]] = dict()

    datasets:List[Dataset] = list()

    try:
        for row in query(connection_str=connection_str,\
                        query=query_info):
            
            schema_name = row[0]

            object_name = row[1]

            object_type = row[2]

            column_name = row[3]

            column_type = row[4]

            key = f"{schema_name}.{object_name}.{object_type}"

            if key not in grouped_column:
                grouped_column[key] = list()

            grouped_column[key].append(
                Column(name=column_name,\
                       type=column_type))
            
        for key in grouped_column:
            
            blocks = key.split(".")

            schema_name = blocks[0]

            object_name = blocks[1]

            object_type = blocks[2]

            datasets.append(
                Dataset(
                    host=host,\
                    database=database,\
                    schema=schema_name,\
                    name=object_name,\
                    type=object_type,\
                    columns=grouped_column[key]
                )
            )


        return datasets


    except:
        return None
