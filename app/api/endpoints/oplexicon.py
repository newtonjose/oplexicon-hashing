from typing import Optional

from fastapi import APIRouter
from pydantic import BaseModel

from app.core.config import config
from oplh.lexicon.opl_reader import OpLexicon
from oplh.models.oplexicon import Result
from oplh.opl_hash import PjwHashing
from oplh.utils import singleton

router = APIRouter()
opl = singleton(lambda: OpLexicon())
pjw = PjwHashing(opl, config.opl_size)


class Response(BaseModel):
    total_lexicons: int
    total_collisions: int
    performance_microseconds: float
    key_infos: Optional[Result]


@router.get('/pjw', response_model=Response)
def get_pjw(key: str = None):
    if key is None:
        return Response(
            total_lexicons=pjw.lexicons,
            total_collisions=pjw.collisions,
            performance_microseconds=pjw.performance,
        )

    return Response(
        total_lexicons=pjw.lexicons,
        total_collisions=pjw.collisions,
        performance_microseconds=pjw.performance,
        key_infos=pjw.get(key)
    )
