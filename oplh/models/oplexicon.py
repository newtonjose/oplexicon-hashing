from enum import Enum

from pydantic import BaseModel


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


class Result(BaseModel):
    data: OplData
    ms: float
