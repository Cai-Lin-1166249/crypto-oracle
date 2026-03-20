import os
import yaml

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class Settings:

    def __init__(self, config_file="config.yaml"):

        with open(config_file, "r") as f:
            config = yaml.safe_load(f)

        # application name
        self.app_name = config["app"]["name"]

        self.provider = config["collector"]["provider"]

        self.cryptos = config["cryptos"]

        # logging config
        self.logging_level = config["logging"]["level"]
        self.log_file = config["logging"]["file"]

        # database url from environment
        self.database_url = os.getenv("DATABASE_URL")

        if not self.database_url:
            raise RuntimeError("DATABASE_URL environment variable not set")


settings = Settings()


# create database engine
engine = create_engine(
    settings.database_url,
    pool_pre_ping=True
)


# create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)