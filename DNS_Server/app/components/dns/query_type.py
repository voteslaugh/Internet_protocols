from enum import Enum


class QueryType(int, Enum):
    A = 1
    NS = 2
    PTR = 12
    AAAA = 28
