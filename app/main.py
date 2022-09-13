from oplh.lexicon.opl_reader import OpLexicon
from oplh.opl_hash import MD5Hashing, MD4Hashing, SHA1Hashing, SHA256Hashing, PjwHashing
from oplh.utils import singleton

from .core.application import create_api

app = create_api()

# if __name__ == '__main__':
#     opl = singleton(lambda: OpLexicon())
#
#     pjw = PjwHashing(opl)
#     # sh1 = SHA1Hashing(opl)
#     # sh2 = SHA256Hashing(opl)
#
#     # print(pjw.get('vulgar'))
#     print(pjw.get('vulgar'))
