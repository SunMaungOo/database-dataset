from dataclasses import dataclass
from typing import List

@dataclass
class Column:
    name:str
    type:str

@dataclass
class Dataset:
    host:str
    database:str
    schema:str
    name:str
    type:str
    columns:List[Column]