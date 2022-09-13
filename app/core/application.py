from fastapi import FastAPI

from app.api.endpoints import oplexicon


def create_api():
    api = FastAPI()

    api.include_router(oplexicon.router)

    return api
