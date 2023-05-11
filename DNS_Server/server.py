from handlers.cache_handler import CacheHandler
from dnslib import DNSRecord, RCODE
import logging


class DNSServer:
    TRUST_SERVER = "8.8.8.8"
    TIMEOUT = 5

    def __init__(self):
        self.cache_handler = CacheHandler()
        self.cache_handler.load("cache")
        self.logger = logging.getLogger(__name__)

    def process(self, query):
        try:
            query_record = DNSRecord.parse(query)
            cache_key = (query_record.q.qtype, query_record.q.qname)
            rdata = self._get_from_cache(cache_key)
            if rdata:
                response = self._create_response(query_record, rdata)
                self.logger.info(f"Found records in cache_handler:\n{response}")
                return response.pack()
            response = self._send_query(query_record)
            if response.header.rcode == RCODE.NOERROR:
                self._update_cache(response)
            return response.pack()
        except Exception as e:
            self.logger.error(f"Error processing query: {e}")
            return None

    def _get_from_cache(self, cache_key):
        rdata = self.cache_handler.get(cache_key)
        return rdata

    def _create_response(self, query_record, rdata):
        response = DNSRecord(header=query_record.header)
        response.add_question(query_record.q)
        response.rr.extend(rdata)
        return response

    def _send_query(self, query_record):
        response = query_record.send(DNSServer.TRUST_SERVER, 53, timeout=DNSServer.TIMEOUT)
        response = DNSRecord.parse(response)
        return response

    def _update_cache(self, response):
        records_by_type = {}
        for rr_section in (response.rr, response.auth, response.ar):
            for rr in rr_section:
                cache_key = (rr.rtype, rr.rname)
                if cache_key not in records_by_type:
                    records_by_type[cache_key] = []
                records_by_type[cache_key].append(rr)
                self.cache_handler.update(cache_key, records_by_type[cache_key], rr.ttl)
