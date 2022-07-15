from pydantic import BaseSettings


class Settings(BaseSettings):
    """
    database_hostname: str = "localhost"
    database_port: str = "5432"
    database_password: str = "kaio123"
    database_name: str = "testando"
    database_username: str = "postgres"
    """
    secret_key_jwt: str = "kaio"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    #heroku muda periodicamente a  url do banco de dados, por isso não da pra quebrar igual acima
    database_url: str = "postgresql://postgres:kaio123@localhost:5432/testando"

    # SQLALCHEMY_DATABASE_URL = f'postgresql://{configuracao.settings.database_username}:{configuracao.settings.database_password}
    # @{configuracao.settings.database_hostname}:{configuracao.settings.database_port}
    # /{configuracao.settings.database_name}'

    class Config:
        env_file = ".env"


settings = Settings()
