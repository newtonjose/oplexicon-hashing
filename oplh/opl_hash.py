from abc import ABC, abstractmethod
from typing import Optional, Dict, Set

from oplh.lexicon.opl_reader import OpLexicon
from oplh.models.oplexicon import OplData
from oplh.utils import Provider, singleton


class OplHashTable(ABC):
    def __init__(self, opl: Provider[OpLexicon]):
        self._opl = opl
        self.collisions = 0
        self._buckets: Dict[int, OplData] = {}
        self._hash_keys: Set[int] = set()

        self._hashing()

    def _hashing(self) -> None:
        for key in self._opl().keys:
            hash_key = self.hash_func(key)

            if hash_key in self._hash_keys:
                self.collisions += 1

            self._buckets[hash_key] = self._opl()[key]
            self._hash_keys.add(hash_key)

    def get(self, key: str) -> Optional[OplData]:
        hash_key = self.hash_func(key)

        if hash_key not in self._hash_keys:
            return None

        return self._buckets[hash_key]

    @abstractmethod
    def hash_func(self, key: str) -> int:
        pass


class ElfHashing(OplHashTable):
    def __init__(self, opl: Provider[OpLexicon]):
        super().__init__(opl)

    def hash_func(self, key: str) -> int:
        """
                        The published hash algorithm used in the UNIX ELF format for object
                        files.  Accepts a string to be hashed and returns an integer
                        :param key:
                        :return:
                        """
        assert isinstance(key, str), 'key: must be a string'

        result = 0
        for c in key:
            result = ((result & 0x0fffffff) << 4) + ord(c)
            x = result & 0xf0000000
            if x != 0:
                result ^= x >> 24
            result &= ~x

        return result


MAX_INT = 0xffffffff
BITS_IN_INT = 8 * 4


class PjwHashing(OplHashTable):
    def __init__(self, opl: Provider[OpLexicon]):
        super().__init__(opl)

    def hash_func(self, key: str) -> int:
        """
        An adaptation of Peter Weinberger's (PJW) generic hashing algorithm based on
        Allen Holub's version.  Accepts a string to be hashed and returns an integer
        :param key:
        :return:
        """
        assert isinstance(key, str), 'key: must be a string'
        three_quarters = int((BITS_IN_INT * 3) / 4)
        one_eighth = int(BITS_IN_INT / 8)
        high_bits = (MAX_INT << (BITS_IN_INT - one_eighth)) & MAX_INT
        hash_value = 0
        for char in key:
            hash_value = (hash_value << one_eighth) + ord(char)
            i = hash_value & 0xF0000000
            if i != 0:
                hash_value = (hash_value ^ (i >> three_quarters)) & ~high_bits
        return hash_value & 0x7fffffff


if __name__ == '__main__':
    opl = singleton(lambda: OpLexicon())

    elf_hash = ElfHashing(opl)
    pjw_hash = PjwHashing(opl)

    print(pjw_hash.get('vulgar'))
