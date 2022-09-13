from abc import abstractmethod, ABCMeta
from datetime import datetime
from typing import Optional, Dict, Set, Tuple, Union

from oplh.functions.hashpy.md4 import MD4
from oplh.functions.hashpy.md5 import MD5
from oplh.functions.hashpy.sha1 import SHA1
from oplh.functions.hashpy.sha2 import SHA256
from oplh.functions.pjw import pjw
from oplh.lexicon.opl_reader import OpLexicon
from oplh.models.oplexicon import OplData, Result
from oplh.utils import Provider


class OplHashTable(metaclass=ABCMeta):
    def __init__(self, opl: Provider[OpLexicon]):
        self._opl = opl
        self.collisions = 0
        self._buckets: Dict[int, OplData] = {}
        self._hash_keys: Set[int] = set()

        time_start, time_end = self._hashing()
        self.performance = (time_end - time_start).total_seconds() * 1000 / len(self._opl().keys)

    def _hashing(self) -> Tuple[datetime, datetime]:
        start = datetime.now()
        for key in self._opl().keys:
            hash_key = self.hash_func(key)

            if hash_key in self._hash_keys:
                self.collisions += 1

            self._buckets[hash_key] = self._opl()[key]
            self._hash_keys.add(hash_key)

        return start, datetime.now()

    def get(self, key: str) -> Optional[Result]:
        start = datetime.now()
        hash_key = self.hash_func(key)

        if hash_key not in self._hash_keys:
            return None

        time_diff = datetime.now() - start
        performance = time_diff.total_seconds() * 1000

        return Result(data=self._buckets[hash_key], ms=performance)

    @abstractmethod
    def hash_func(self, key: str) -> Union[int, hex]:
        pass

    def update(self, data):
        pass


class PjwHashing(OplHashTable):
    def __init__(self, opl: Provider[OpLexicon]):
        super().__init__(opl)

    def hash_func(self, key: str) -> int:
        return pjw(key)


class MD5Hashing(OplHashTable):
    def __init__(self, opl: Provider[OpLexicon]):
        super().__init__(opl)

    def hash_func(self, key: str) -> Union[int, str]:
        assert isinstance(key, str), 'key: must be a string'

        md5 = MD5(key)

        return md5.hexdigest


class MD4Hashing(OplHashTable):
    def __init__(self, opl: Provider[OpLexicon]):
        super().__init__(opl)

    def hash_func(self, key: str) -> Union[int, str]:
        assert isinstance(key, str), 'key: must be a string'

        md5 = MD4(key)

        return md5.hexdigest


class SHA1Hashing(OplHashTable):
    def __init__(self, opl: Provider[OpLexicon]):
        super().__init__(opl)

    def hash_func(self, key: str) -> Union[int, str]:
        assert isinstance(key, str), 'key: must be a string'

        sha1 = SHA1(key)

        return sha1.hexdigest()


class SHA256Hashing(OplHashTable):
    def __init__(self, opl: Provider[OpLexicon]):
        super().__init__(opl)

    def hash_func(self, key: str) -> Union[int, str]:
        assert isinstance(key, str), 'key: must be a string'

        sh = SHA256(key)

        return sh.hexdigest()
