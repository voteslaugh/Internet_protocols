from dataclasses import dataclass


@dataclass
class DNSHeader:
    id: int
    flags: int
    qd_count: int
    an_count: int
    ns_count: int
    ar_count: int