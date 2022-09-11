import codecs
from enum import Enum
from pathlib import Path
from typing import List, Set

from pydantic import BaseModel

from oplh.settings import Config

config = Config(opl_path='/home/th3clansman/Development/projects/oplexicon-hashing/data/lexico_v3.0.txt')


class KeyTypes(Enum):
    ADJ = "adj"
    NOM = "nom"
    VERB = "vb"
    VB_DET = "vb det n prp"
    VB_PRP = "vb n prp"
    VB_ADV = "vb adv"
    VB_ADJ = "vb adj"
    EMOT = "emot"
    HTAG = "htag"


class InputTypes(Enum):
    AUTOMATIC = "A"
    MANUAL = "M"


class OplData(BaseModel):
    key: str
    pos: KeyTypes
    pol: int
    input_type: InputTypes


class OpLexicon(dict):
    def __init__(self):
        super().__init__()

        self.keys: Set[str] = set()

    def parser_file(self) -> None:
        f = codecs.open(config.opl_path, 'r', 'utf-8')

        line = f.readline().strip()
        while line:
            if not len(line) == 0:
                try:
                    word, pos, pol, input_type = line.split(',')

                    data = OplData(key=word, pos=KeyTypes(pos), pol=int(pol), input_type=InputTypes(input_type))
                    self._append_data(data)
                except Exception as e:
                    raise IOError(f"Error parsing the file on line: {line}\nError: {str(e)}")

            line = f.readline().strip()

        f.close()

    def _append_data(self, data):
        self.keys.add(data.key)
        self[data.key] = list(data)


if __name__ == '__main__':
    opl = OpLexicon()
    opl.parser_file()


