from dataclasses import dataclass
from query_type import QueryType
from query_class import QueryClass


@dataclass
class DNSQuestion:
    q_name: str
    q_type: QueryType
    q_class: QueryClass
