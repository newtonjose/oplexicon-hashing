from abc import abstractmethod, ABCMeta
from datetime import datetime
from typing import Optional, Dict, Set, Tuple, Union, List

from oplh.functions.hashpy.md4 import MD4
from oplh.functions.hashpy.md5 import MD5
from oplh.functions.hashpy.sha1 import SHA1
from oplh.functions.hashpy.sha2 import SHA256
from oplh.functions.pjw import pjw
from oplh.lexicon.opl_reader import OpLexicon
from oplh.models.oplexicon import OplData, Result
from oplh.utils import Provider


class OplHashTable(metaclass=ABCMeta):
    def __init__(self, opl: Provider[OpLexicon], lexicons: int = 0):
        self._opl = opl
        self.collisions = 0
        self.table_size = 42209
        self.buckets: List[Optional[OplData]] = [None] * self.table_size
        self.lexicons: int = lexicons if lexicons else len(self._opl().keys)
        self.spread_collisions = {}

        time_start, time_end = self._hashing()

        self.performance = (time_end - time_start).total_seconds() * 1000 / self.lexicons

    def _hashing(self) -> Tuple[datetime, datetime]:
        start = datetime.now()
        limit = self.lexicons
        for key in self._opl().keys:
            index = self.hash_func(key) % self.table_size

            bucket = self.buckets[index]
            if bucket is not None:
                self.collisions += 1
                self.spread_collisions.update({f"{index}": self.spread_collisions.get(f"{index}", 0) + 1})

                while bucket is not None:
                    index += 1
                    if index == self.table_size:
                        index = 0

                    bucket = self.buckets[index]

            self.buckets[index] = self._opl()[key]

            limit -= 1
            if limit == 0:
                break

        return start, datetime.now()

    def get(self, key: str) -> Optional[Result]:
        start_time = datetime.now()
        index = self.hash_func(key) % self.table_size

        bucket = self.buckets[index]
        while bucket is not None and bucket.key != key:
            index += 1
            bucket = self.buckets[index]

        if bucket is None:
            return None

        end_time = datetime.now()
        time_diff = end_time - start_time
        performance = time_diff.total_seconds() * 1000

        return Result(data=bucket, ms=performance)

    @abstractmethod
    def hash_func(self, key: str) -> int:
        pass


class PjwHashing(OplHashTable):
    def __init__(self, opl: Provider[OpLexicon], limit):
        super().__init__(opl, limit)

    def hash_func(self, key: str) -> int:
        return pjw(key)


class MD5Hashing(OplHashTable):
    def __init__(self, opl: Provider[OpLexicon], limit):
        super().__init__(opl, limit)

    def hash_func(self, key: str) -> Union[int, str]:
        assert isinstance(key, str), 'key: must be a string'

        md5 = MD5(key)

        return int('0x' + md5.hexdigest, 0)


class MD4Hashing(OplHashTable):
    def __init__(self, opl: Provider[OpLexicon], limit):
        super().__init__(opl, limit)

    def hash_func(self, key: str) -> Union[int, str]:
        assert isinstance(key, str), 'key: must be a string'

        md5 = MD4(key)

        return int('0x' + md5.hexdigest, 0)


class SHA1Hashing(OplHashTable):
    def __init__(self, opl: Provider[OpLexicon], limit):
        super().__init__(opl, limit)

    def hash_func(self, key: str) -> Union[int, str]:
        assert isinstance(key, str), 'key: must be a string'

        sha1 = SHA1(key)
        return int('0x' + sha1.hexdigest(), 0)


class SHA256Hashing(OplHashTable):
    def __init__(self, opl: Provider[OpLexicon], limit):
        super().__init__(opl, limit)

    def hash_func(self, key: str) -> Union[int, str]:
        assert isinstance(key, str), 'key: must be a string'

        sh = SHA256(key)

        return int('0x' + sh.hexdigest(), 0)
