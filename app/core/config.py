from pydantic import BaseSettings


class Config(BaseSettings):
    service_name: str = 'service_name'
    secret_key: str = 's3cr3t_k3y'
    opl_size: int = 0


config = Config()
