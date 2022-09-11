import codecs
from typing import Set

from oplh.models.oplexicon import OplData, KeyTypes, InputTypes
from oplh.settings import Config
from oplh.utils import singleton

config = Config(opl_path='/home/th3clansman/Development/projects/oplexicon-hashing/data/lexico_v3.0.txt')


class OpLexicon(dict):
    def __init__(self):
        super().__init__()

        self.keys: Set[str] = set()
        self._parser_file()

    def _parser_file(self) -> None:
        f = codecs.open(config.opl_path, 'r', 'utf-8')

        line = f.readline().strip()
        while line:
            if not len(line) == 0:
                try:
                    word, pos, pol, input_type = line.split(',')

                    data = OplData(key=word, pos=KeyTypes(pos), pol=int(pol), input_type=InputTypes(input_type))
                    self.keys.add(data.key)
                    self[data.key] = data
                except Exception as e:
                    raise IOError(f"Error parsing the file on line: {line}\nError: {str(e)}")

            line = f.readline().strip()

        f.close()

