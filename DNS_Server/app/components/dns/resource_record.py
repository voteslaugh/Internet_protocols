from dataclasses import dataclass
from query_class import QueryClass
from query_type import QueryType


@dataclass
class DNSResourceRecord:
    r_name: str
    r_type: QueryType
    r_class: QueryClass
    r_ttl: int
    rd_length: int
    r_data: str