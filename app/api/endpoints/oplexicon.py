from typing import Optional

from fastapi import APIRouter
from pydantic import BaseModel

from app.core.config import config
from oplh.lexicon.opl_reader import OpLexicon
from oplh.models.oplexicon import Result
from oplh.opl_hash import PjwHashing, MD4Hashing, MD5Hashing, SHA1Hashing, SHA256Hashing
from oplh.utils import singleton

router = APIRouter()
opl = singleton(lambda: OpLexicon())
pjw = PjwHashing(opl, config.opl_size)
md4 = MD4Hashing(opl, config.opl_size)
md5 = MD5Hashing(opl, config.opl_size)
sha1 = SHA1Hashing(opl, config.opl_size)
sha2 = SHA256Hashing(opl, config.opl_size)


class Response(BaseModel):
    total_lexicons: int
    total_collisions: int
    performance_microseconds: float
    spread_collisions: Optional[dict]
    key_infos: Optional[Result]


@router.get('/pjw', response_model=Response)
def get_pjw(key: str = None):
    if key is None:
        return Response(
            total_lexicons=pjw.lexicons,
            total_collisions=pjw.collisions,
            performance_microseconds=pjw.performance,
            spread_collisions=pjw.spread_collisions,
        )

    return Response(
        total_lexicons=pjw.lexicons,
        total_collisions=pjw.collisions,
        performance_microseconds=pjw.performance,
        key_infos=pjw.get(key)
    )


@router.get('/md4', response_model=Response)
def get_md4(key: str = None):
    if key is None:
        return Response(
            total_lexicons=md4.lexicons,
            total_collisions=md4.collisions,
            performance_microseconds=md4.performance,
            spread_collisions=md4.spread_collisions,
        )

    return Response(
        total_lexicons=md4.lexicons,
        total_collisions=md4.collisions,
        performance_microseconds=md4.performance,
        key_infos=md4.get(key)
    )


@router.get('/md5', response_model=Response)
def get_md5(key: str = None):
    if key is None:
        return Response(
            total_lexicons=md5.lexicons,
            total_collisions=md5.collisions,
            performance_microseconds=md5.performance,
            spread_collisions=md5.spread_collisions,
        )

    return Response(
        total_lexicons=md5.lexicons,
        total_collisions=md5.collisions,
        performance_microseconds=md5.performance,
        key_infos=md5.get(key)
    )


@router.get('/sha1', response_model=Response)
def get_sha1(key: str = None):
    if key is None:
        return Response(
            total_lexicons=sha1.lexicons,
            total_collisions=sha1.collisions,
            performance_microseconds=sha1.performance,
            spread_collisions=sha1.spread_collisions,
        )

    return Response(
        total_lexicons=sha1.lexicons,
        total_collisions=sha1.collisions,
        performance_microseconds=sha1.performance,
        key_infos=sha1.get(key)
    )


@router.get('/sha2', response_model=Response)
def get_sha2(key: str = None):
    if key is None:
        return Response(
            total_lexicons=sha2.lexicons,
            total_collisions=sha2.collisions,
            performance_microseconds=sha2.performance,
            spread_collisions=sha2.spread_collisions,
        )

    return Response(
        total_lexicons=sha2.lexicons,
        total_collisions=sha2.collisions,
        performance_microseconds=sha2.performance,
        key_infos=sha2.get(key)
    )


@router.get('/spread_collisions')
def get_pjw_csv(algorith: str = None):
    if algorith == "pjw":
        data = pjw.spread_collisions
    elif algorith == "md4":
        data = md4.spread_collisions
    elif algorith == "md5":
        data = md5.spread_collisions
    elif algorith == "sha1":
        data = sha1.spread_collisions
    elif algorith == "sha2":
        data = sha2.spread_collisions
    else:
        data = {}

    with open('./data/spread_collisions.csv', 'w') as f:
        for key, val in data.items():
            f.write("%s,%s\n" % (key, val))