from pydantic_settings import BaseSettings
from sqlalchemy.engine.url import URL


class Settngs(BaseSettings):
    debug: bool = False
    app_port: int = 8000

    db_driver: str = "postgresql+asyncpg"
    db_host: str = "db"
    db_port: int = 5432
    db_database: str = "postgres"
    db_user: str = "postgres"
    db_password: str = "password"

    db_echo: bool = False
    db_pool_pre_ping: bool = True


    @property
    def db_dsn(self) -> URL:
        return URL.create(
            self.db_driver,
            self.db_user,
            self.db_password,
            self.db_host,
            self.db_port,
            self.db_database,
        )


settings = Settngs()