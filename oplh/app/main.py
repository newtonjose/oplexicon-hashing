from oplh.lexicon.opl_reader import OpLexicon
from oplh.opl_hash import MD5Hashing
from oplh.utils import singleton

if __name__ == '__main__':
    opl = singleton(lambda: OpLexicon())

    md5 = MD5Hashing(opl)
    # pjw_hash = PjwHashing(opl)

    print(md5.get('vulgar'))
    # print(pjw_hash.get('vulgar'))
