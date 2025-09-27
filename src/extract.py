from database import get_connection_string,test_connection
from config import HOST_NAME,DATABASE_NAME,USER_NAME,PASSWORD,PORT,OUTPUT_FILE_PATH
import logging
import sys
from connector import get_dataset
from dataclasses import asdict
import json
from pathlib import Path

logger = logging.getLogger("database-dataset")

logger.setLevel(logging.DEBUG)

# Prevent propagation to root logger (avoids duplicate logs if used in packages)
logger.propagate = False

formatter = logging.Formatter(
    fmt='%(asctime)s | %(levelname)-8s | %(name)-15s | %(lineno)-3d | %(message)s',
    datefmt='%Y-%m-%dT%H:%M:%S' 
)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

logger.addHandler(console_handler)

def main()->int:
    connection_str = get_connection_string(host=HOST_NAME,\
                          database_name=DATABASE_NAME,\
                          user=USER_NAME,\
                          password=PASSWORD,\
                          port=PORT)
    
    logger.info("Testing connection to database")
    
    is_db_connected = test_connection(connection_str=connection_str)

    if not is_db_connected:
        logger.info("Cannot connect to the database.Please check the database configuration")
        return -1
    
    else:
        logger.info("Connection to database success")

    logger.info("Extracting dataset")

    datasets = get_dataset(connection_str=connection_str,\
                           host=HOST_NAME,\
                           database=DATABASE_NAME)
    
    if datasets is None:
        logger.info("Extracting dataset:fail")
        return -1

    logger.info("Extracting dataset:sucesss")

    logger.info(f"Dataset Extracted:{len(datasets)}")


    try:

        output_file_path = Path(OUTPUT_FILE_PATH)
        output_file_path.parent.mkdir(parents=True,exist_ok=True)

        with output_file_path.open(mode="w") as file:
            json.dump([asdict(dataset) for dataset in datasets],file,indent=4)

        logger.info(f"Saving dataset to {OUTPUT_FILE_PATH}:success")

    except:
        logger.info(f"Saving dataset to {OUTPUT_FILE_PATH}:fail")

        return -1

    return 0

if __name__=="__main__":
    sys.exit(main())