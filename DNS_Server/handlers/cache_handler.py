import pickle
import time


class CacheHandler:
    def __init__(self):
        self.cache = None

    def save(self, path):
        with open(path, "wb") as dump:
            pickle.dump(self.cache, dump)

    def load(self, path):
        try:
            with open(path, "rb") as dump:
                data = pickle.load(dump)
                if data:
                    self.cache = data
        except FileNotFoundError:
            self.cache = {}

    def update(self, key, records, ttl):
        total_ttl = time.time() + ttl
        self.cache[key] = (records, total_ttl)

    def get(self, key):
        data = self.cache.get(key)
        if data is None:
            return
        rdata, ttl = data
        if time.time() > ttl:
            del self.cache[key]
        return rdata
