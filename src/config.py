from decouple import config

INVALID_PORT = -1

OUTPUT_FILE_PATH = config("OUTPUT_FILE_PATH",cast=str,default="dataset.json")

HOST_NAME = config("HOST_NAME",cast=str)

DATABASE_NAME = config("DATABASE_NAME",cast=str)

PORT = config("PORT",cast=int,default=INVALID_PORT)

USER_NAME = config("USER_NAME",cast=str)

PASSWORD = config("PASSWORD",cast=str)

DB_TYPE = config("DB_TYPE",cast=str,default="mssql")

IS_SID = False

if DB_TYPE=="oracle":
    IS_SID = config("IS_SID",cast=bool,default=False)

MSSQL_DEFAULT_PORT = 1433

ORACLE_DEFAULT_PORT = 1521

MSSQL_GET_INFO_SQL = """

SELECT column_info.TABLE_SCHEMA AS SCHEMA_NAME,
column_info.TABLE_NAME AS TABLE_NAME,
table_info.TABLE_TYPE,
column_info.COLUMN_NAME,
CASE
	WHEN column_info.DATA_TYPE_LENGTH IS NULL
	THEN CONCAT(column_info.DATA_TYPE,' ',IS_NULLABLE)
	ELSE CONCAT(column_info.DATA_TYPE,DATA_TYPE_LENGTH,' ',IS_NULLABLE)
END AS COLUMN_DATA_TYPE
FROM
(

	SELECT TABLE_SCHEMA,
	TABLE_NAME,
	COLUMN_NAME,
	DATA_TYPE,
	CASE
		WHEN DATA_TYPE IN 
		(
			'char',
			'varchar',
			'nchar',
			'nvarchar'
		)
		THEN 
			CASE
				WHEN CHARACTER_MAXIMUM_LENGTH = -1
				THEN '(max)'
				ELSE CONCAT('(',CAST(CHARACTER_MAXIMUM_LENGTH AS nvarchar(10)),')')
			END
		WHEN DATA_TYPE IN 
		(
			'decimal',
			'numeric'
		)
		THEN  CONCAT('(',CAST(NUMERIC_PRECISION AS nvarchar(10)),',',CAST(NUMERIC_SCALE AS nvarchar(10)),')')
		ELSE NULL
	END AS DATA_TYPE_LENGTH,
	CASE IS_NULLABLE
		WHEN 'YES'
		THEN 'null'
		ELSE 'not null'
	END AS IS_NULLABLE
	FROM INFORMATION_SCHEMA.COLUMNS
)AS column_info
INNER JOIN 
(
	SELECT TABLE_SCHEMA,
	TABLE_NAME,
	CASE TABLE_TYPE
		 WHEN 'BASE TABLE'
		 THEN 'table'
		 WHEN 'VIEW'
		 THEN 'view'
	END AS TABLE_TYPE
	FROM INFORMATION_SCHEMA.TABLES
) AS table_info
ON column_info.TABLE_SCHEMA = table_info.TABLE_SCHEMA
AND column_info.TABLE_NAME = table_info.TABLE_NAME

"""

ORACLE_GET_INFO_SQL = """

WITH column_info AS 
(
    SELECT OWNER AS SCHEMA_NAME,
    TABLE_NAME,
    COLUMN_NAME,
    DATA_TYPE,
    CASE
        WHEN DATA_TYPE IN 
        (
            'CHAR',
            'VARCHAR2',
            'NCHAR',
            'NVARCHAR2'
        )
        THEN
            CASE 
                WHEN CHAR_USED = 'C'
                THEN '(' || CHAR_LENGTH || ')'
                ELSE '(' || DATA_LENGTH || ')'
            END
        WHEN DATA_TYPE = 'RAW'
        THEN '(' || DATA_LENGTH || ')'
        WHEN DATA_TYPE = 'NUMBER'
        THEN 
            CASE
                WHEN DATA_PRECISION IS NOT NULL 
                THEN '(' || DATA_PRECISION || ',' || DATA_SCALE || ')'
            END    
    END AS DATA_TYPE_LENGTH,
    CASE NULLABLE
      WHEN 'Y'
      THEN 'null'
      ELSE 'not null'
    END AS IS_NULLABLE 
    FROM ALL_TAB_COLUMNS
),table_info AS 
(
    SELECT OWNER AS SCHEMA_NAME,
    OBJECT_NAME AS TABLE_NAME,
    CASE OBJECT_TYPE
        WHEN 'TABLE'
        THEN 'table'
        WHEN 'VIEW'
        THEN 'view'
    END AS TABLE_TYPE
    FROM ALL_OBJECTS
    WHERE OBJECT_TYPE IN 
    (
        'TABLE',
        'VIEW'
    )
)
SELECT column_info.SCHEMA_NAME,
column_info.TABLE_NAME,
table_info.TABLE_TYPE,
column_info.COLUMN_NAME,
CASE
    WHEN column_info.DATA_TYPE_LENGTH IS NULL
	THEN column_info.DATA_TYPE || ' ' || IS_NULLABLE
	ELSE column_info.DATA_TYPE || DATA_TYPE_LENGTH || ' ' || IS_NULLABLE
END AS COLUMN_DATA_TYPE
FROM column_info
INNER JOIN table_info
ON column_info.SCHEMA_NAME = table_info.SCHEMA_NAME
AND column_info.TABLE_NAME = table_info.TABLE_NAME

"""