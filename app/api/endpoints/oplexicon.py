from fastapi import APIRouter
from pydantic import BaseModel

from app.core.logger import logger
from oplh.lexicon.opl_reader import OpLexicon
from oplh.opl_hash import PjwHashing
from oplh.utils import singleton

router = APIRouter()
opl = singleton(lambda: OpLexicon())

pjw = PjwHashing(opl)


class Response(BaseModel):
    total_lexicons: int
    total_collisions: int
    performance_microseconds: float


@router.get('/pjw', response_model=Response)
def get_pjw():
    logger.info('This is an example of logging')

    return Response(
        total_lexicons=pjw.lexicons,
        total_collisions=pjw.collisions,
        performance_microseconds=pjw.performance,
    )
