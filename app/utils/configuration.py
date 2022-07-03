import envtoml
from app.utils.logger import Logger
from app.utils.utitlity_classes import Singleton


class Config(metaclass=Singleton):
    def __init__(self, path: str = "config.toml", logger=None):
        self.path = path
        self.log: Logger = self.get_logger

    @property
    def conf(self):
        from pathlib import Path

        conf_file: Path = Path(self.path)
        with conf_file.open(mode="r") as toml_string:
            parsed_toml = envtoml.loads(toml_string.read())
            return parsed_toml

    @property
    def get_logger(self) -> Logger:
        return Logger(self.conf.get("log_level"))

    @property
    def app_env(self):
        return self.conf.get("app_env")

    @property
    def db_url(self):
        return (
            self.conf.get("database_url")
            if self.conf.get("app_env") == "dev" or self.conf.get("app_env") == "prod"
            else self.conf.get("test_database_url")
        )

    @property
    def token_validity_period(self):
        return self.conf.get("token_validity_period")

    @property
    def jwt_secret(self):
        return self.conf.get("jwt_secret")

    @property
    def hash_algorithm(self):
        return self.conf.get("hash_algorithm")
