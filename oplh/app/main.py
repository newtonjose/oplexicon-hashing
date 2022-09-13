from oplh.lexicon.opl_reader import OpLexicon
from oplh.opl_hash import MD5Hashing, MD4Hashing, SHA1Hashing, SHA256Hashing, PjwHashing
from oplh.utils import singleton

if __name__ == '__main__':
    opl = singleton(lambda: OpLexicon())

    pjw = PjwHashing(opl)
    sh = SHA1Hashing(opl)
    # pjw_hash = PjwHashing(opl)

    print(pjw.get('vulgar'))
    print(sh.get('vulgar'))
    # print(pjw_hash.get('vulgar'))
